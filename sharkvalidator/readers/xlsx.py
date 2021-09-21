# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institut.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-12-15 13:59

@author: johannes
"""
import pandas as pd
from sharkvalidator.readers.reader import Reader


class PandasReaderBase(Reader):
    """Base Class for pandas reader."""

    def __init__(self, *args, **kwargs):
        """Initialize."""
        super().__init__()

    def get(self, item):
        """Return value for item."""
        if item in self.__dict__.keys():
            return self.__getattribute__(item)
        else:
            print('Warning! Can´t find attribute: %s' % item)
            return 'None'

    @staticmethod
    def _activate_file(*args, **kwargs):
        """Return activated excel file."""
        return pd.ExcelFile(*args, **kwargs)

    @staticmethod
    def read(*args, **kwargs):
        """Return pandas.DataFrame."""
        return pd.read_excel(*args, **kwargs).fillna('')


class PandasXlsxReader(PandasReaderBase):
    """Read xlsx files."""

    def __init__(self, *args, **kwargs):
        """Initialize."""
        super().__init__()
        self.arguments = list(args)
        for key, item in kwargs.items():
            setattr(self, key, item)
        self.file = None

    def load(self, *args, **kwargs):
        """Activate file."""
        self.file = self._activate_file(*args, **kwargs)

    def read_element(self, *args, **kwargs):
        """Read data element.

        Reading excel sheet into pandas.Dataframe.
        """
        return self._read_sheet(*args, **kwargs)

    def _read_sheet(self, *args, **kwargs):
        """Read excel sheet and return pandas.DataFrame."""
        sheet = args[0] if type(args) == tuple else args
        if sheet in self.file.sheet_names:
            if kwargs.get('dtype') == '':
                kwargs['dtype'] = str
            df = self.file.parse(*args, **kwargs).fillna('')
            df = self.eliminate_empty_rows(df)
        else:
            df = None
            print('sheet {} not found in delivery'.format(sheet))
        return df
