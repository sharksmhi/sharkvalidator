# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-12-15 14:10

@author: johannes

"""
from sharkvalidator.config import Settings
from sharkvalidator.handler import DataFrames, MultiDeliveries
from sharkvalidator.validators.validator import ValidatorLog


class App:
    """
    Keep it clean, keep it tidy!
    - read
    - validate
    - write log

    Only for validation! Do not pass data on to other tasks!

    Beautiful is better than ugly.
    Readability counts.

    """
    def __init__(self, *args, **kwargs):
        self.settings = Settings(**kwargs)
        self.deliveries = MultiDeliveries()

    def read(self, *args, reader=None, delivery_name=None, **kwargs):
        """

        :param args:
        :param reader:
        :param delivery_name:
        :param kwargs:
        :return:
        """
        assert reader
        assert args

        reader = self.settings.load_reader(reader)
        delivery_name = delivery_name

        reader.load(*args, **kwargs)

        dfs = DataFrames(data_type=reader.get('data_type'), name=delivery_name)
        for element, item in reader.elements.items():
            df = reader.read_element(item.pop('element_specifier'), **item)
            dfs.append_new_frame(name=element, data=df)

        self.deliveries.append_new_delivery(name=delivery_name, data=dfs)

    def validate(self, *args, validator_list=None, **kwargs):
        """"""
        validator_list = validator_list or self.settings.validators_sorted
        for validator_name in validator_list:
            validator = self.settings.load_validator(validator_name)
            for delivery_name in args:
                validator.validate(self.deliveries.get(delivery_name), **kwargs)

    def write(self, *args, writer=None, **kwargs):
        """"""
        assert writer

        writer = self.settings.load_writer(writer)
        kwargs.setdefault('default_file_name', writer.default_file_name)
        file_path = self.settings.get_export_file_path(**kwargs)

        writer.write(file_path, **kwargs)
        print('Writer done!')
