# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-12-15 14:10

@author: johannes

"""



class App:
    """
    Keep it clean, keep it tidy!
    - read
    - validate
    - write
    """
    def __init__(self, *args, **kwargs):
        self.settings = Settings(**kwargs)

    def validate(self, *args, **kwargs):
        """
        :param args:
            Expects:
                list_name(s)
        :param kwargs:
            Addition:
                validator_list
        :return:
        """
        validator_list = kwargs.get('validator_list') or self.settings.validators_sorted
        for list_name in args:
            for validator_name in validator_list:
                validator = self.settings.load_validator(validator_name)
                validator.validate(self.lists.select(list_name), master=self.lists.select('master'))

    def read(self, *args, **kwargs):
        """
        :param args: tuple
            Expects:
                file_path
        :param kwargs: dict
            Expects:
                reader
        :return:
        """
        assert 'reader' in kwargs
        assert args

        reader = self.settings.load_reader(kwargs.get('reader'))
        list_name = kwargs.get('list_name')
        for pop_key in ('list_name', 'reader'):
            kwargs.pop(pop_key)

        lst = reader.read(*args, **kwargs)



if __name__ == '__main__':
    app = App()
    app.read_list(
        'C:/Arbetsmapp/config/station.txt',
        header=0,
        sep='\t',
        encoding='cp1252',
        dtype=str,
        keep_default_na=False,
        reader='shark_master',
        list_name='master',
    )