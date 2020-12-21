# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-12-15 14:15

@author: johannes

"""
import pandas as pd
from sharkvalidator.readers.xlsx import PandasXlsxReader


class PhysicalChemicalExcelReader(PandasXlsxReader):
    """
    """
    def __init__(self, *args, **kwargs):
        super(PhysicalChemicalExcelReader, self).__init__(*args, **kwargs)
        self.arguments = list(args)

        self.file = None

    def read(self, *args, **kwargs):
        """
        :param file_path:
        :return:
        """
        self.file = pd.ExcelFile(*args, **kwargs)

    def read_sheet(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        return self.file.parse(*args, **kwargs)


if __name__ == '__main__':
    p = PhysicalChemicalExcelReader(2, 5, 6, a='g', b=33)
    p.read('C:/Arbetsmapp/webmtrl/Format Physical and chemical.xlsx')
    df = p.read_sheet(
        'Analysinfo',
        header=2,
        sep='\t',
        dtype=str,
        keep_default_na=False,
    )
