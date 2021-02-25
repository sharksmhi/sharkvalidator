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
        Read and append requested data delivery.

        Using the given reader (name of reader) to load and initialize a reader object via Settings.
        Elements of the data delivery are put into Frame objects and collected into a delivery dictionary
        Args:
            delivery path (in *args): path to delivery (str)
            reader (str): One of the readers found in self.settings.list_of_readers
            delivery_name (str): Chosen name of delivery. Used as key in self.deliveries
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

    def validate(self, *args, validator_list=None, disapproved_only=False, **kwargs):
        """
        Validate x number of deliveries using y number of validators.

        Validation results are stored in validators.validator.ValidatorLog
        Args:
            *args: (tuple): Contains delivery names.
            disapproved_only (bool): If set to True the ValidatorLog will only include disapproved validation
                                     information.
            validator_list (None or list): One or more validators to use in order to validate data delivery/deliveries.
                                           Available validators can be found in self.settings.list_of_validators.
                                           If no validator_list is given we use all available validators in
                                           self.settings.validators_sorted
        """
        validator_list = validator_list or self.settings.validators_sorted
        for validator_name in validator_list:
            validator = self.settings.load_validator(validator_name)
            for delivery_name in args:
                validator.validate(
                    self.deliveries.get(delivery_name),
                    disapproved_only=disapproved_only,
                    **kwargs,
                )

    def write(self, *args, writer=None, **kwargs):
        """
        Write log.
        Using the given writer (name of writer) to load and initialize a writer object via Settings.

        Args:
            writer (str): Using the given writer to write log to file.
                          Available writers can be found in self.settings.list_of_writers
        """
        assert writer

        writer = self.settings.load_writer(writer)
        kwargs.setdefault('default_file_name', writer.default_file_name)
        file_path = self.settings.get_export_file_path(**kwargs)

        writer.write(file_path, **kwargs)
        print('Writer done!')
