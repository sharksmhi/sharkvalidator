# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-12-15 13:59

@author: johannes

"""
import pandas as pd


class PandasReaderBase:
    """
    """
    def __init__(self, *args, **kwargs):
        super(PandasReaderBase, self).__init__()

    def get(self, item):
        """
        :param item: str
        :return:
        """
        if item in self.__dict__.keys():
            return self.__getattribute__(item)
        else:
            print('Warning! Can´t find attribute: %s' % item)
            return 'None'

    @staticmethod
    def activate_file(*args, **kwargs):
        """
        xl = pd.ExcelFile('foo.xls')
        xl.sheet_names  # see all sheet names
        xl.parse(sheet_name)  # read a specific sheet to DataFrame
        :param args:
        :param kwargs:
        :return:
        """
        return pd.ExcelFile(*args, **kwargs)

    @staticmethod
    def read(*args, **kwargs):
        """
        :param args: tuple
            Expects:
                file_path
        :param kwargs: dict
            Addition:
                header
                encoding
                dtype
                keep_default_na
        :return:
        """
        return pd.read_excel(*args, **kwargs)


class PandasXlsxReader(PandasReaderBase):
    """
    Reads xlsx files
    """
    def __init__(self, *args, **kwargs):
        super(PandasXlsxReader, self).__init__()
        for key, item in kwargs.items():
            setattr(self, key, item)
