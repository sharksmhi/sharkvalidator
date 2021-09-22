# Copyright (c) 2021 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).
"""
Created on 2021-01-07 11:15

@author: johannes
"""
from sharkvalidator.readers.xlsx import PandasXlsxReader


class PhytoplanktonExcelReader(PandasXlsxReader):
    """Reader for the Phytoplankton datatype."""

    # TODO We probably need to extend this class? or maybe not..

    def __init__(self, *args, **kwargs):
        """Initialize."""
        super().__init__(*args, **kwargs)
