# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-12-15 14:15

@author: johannes

"""
import pandas as pd


class PhysicalChemicalExcelReader:
    """
    """
    def __init__(self, *args, **kwargs):
        self.arguments = args
        for key, item in kwargs.items():
            setattr(self, key, item)


if __name__ == '__main__':
    p = PhysicalChemicalExcelReader(2, 5, 6, a='g', b=33)
