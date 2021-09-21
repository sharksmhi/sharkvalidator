# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-12-15 14:00

@author: johannes
"""
from sharkvalidator.readers.txt import PandasTxtReader, text_reader  # noqa: F401
from sharkvalidator.readers.yml import yaml_reader  # noqa: F401
from sharkvalidator.readers.xlsx import PandasXlsxReader  # noqa: F401
from sharkvalidator.readers.phyche import PhysicalChemicalExcelReader, PhysicalChemicalLIMSReader  # noqa: F401
from sharkvalidator.readers.phytop import PhytoplanktonExcelReader  # noqa: F401
from sharkvalidator.readers.shark import SharkwebReader, SharkzipReader  # noqa: F401
