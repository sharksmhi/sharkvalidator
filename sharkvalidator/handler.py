# Copyright (c) 2021 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-01-05 09:38

@author: johannes

"""
from abc import ABC
import pandas as pd
from sharkvalidator.utils import TranslateHeader, TranslateParameters


class Frame(pd.DataFrame, ABC):
    """
    Stores data from one, and only one, element (usually an excel sheet or a txt file).
    """
    @property
    def _constructor(self):
        """
        Constructor for Frame, overides method in pandas.DataFrame
        """
        return Frame

    def convert_formats(self):
        self[self.data_columns] = self[self.data_columns].astype(float)

    def translation(self):
        self.rename(columns=TranslateHeader.data, inplace=True)
        if 'PARAM' in self.columns:
            self['PARAM'] = self['PARAM'].apply(lambda x: TranslateParameters.map_get(x))

    @property
    def data_columns(self):
        #FIXME: nicht correcto.. how to extract only data columns (without using hardcoded parts or index ! ! !).
        # Do we use settingfile? perhaps..
        # Or! from Q_flag-fields? but then we rely on a perfect delivery
        # return [c for c in self.columns if not c.startswith('Q_')]
        return [c[2:] for c in self.quality_flag_columns]

    @property
    def quality_flag_columns(self):
        return [c for c in self.columns if c.startswith('Q_')]


class DataFrames(dict):
    """
    Stores information for delivery elements (sheets / files, eg. delivery_info, data, analyse_info, sampling_info).
    Use element name as key in this dictionary of Frame()-objects
    """
    def __init__(self, **kwargs):
        super(DataFrames, self).__init__()
        for key, item in kwargs.items():
            setattr(self, key, item)

    def append_new_frame(self, name=None, data=None, **kwargs):
        if name:
            # print('New data added for {}'.format(name))
            self.setdefault(name, Frame(data))
            self[name].translation()
            # self[name].convert_formats()
            # self[name].exclude_flagged_data()


class MultiDeliveries(dict):
    """
    Not sure about the functionality of this class..
    Perhaps we can settle with just an ordinary dictionary..
    Time will tell..
    """
    def append_new_delivery(self, name=None, data=None, **kwargs):
        delivery_name = name
        if delivery_name:
            # print('New data added for {}'.format(name))
            self.setdefault(delivery_name, data)

    def drop_delivery(self, name=None):
        if name in self:
            self.pop(name)
