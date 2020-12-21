# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-12-16 13:52

@author: johannes

"""
import pandas as pd
from sharkvalidator.validators.validator import Validator, ValidatorLog


class ExcelDeliveryFormat(Validator):
    """
    """
    def __init__(self, *args, **kwargs):
        super(ExcelDeliveryFormat, self).__init__(*args, **kwargs)
        for key, item in kwargs.items():
            setattr(self, key, item)

    def validate(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        assert self.reader
        assert self.sheets

        report = {'approved': {},
                  'disapproved': {}}

        for sheet in self.sheets:
            if sheet in self.reader.file.sheet_names:
                report['approved'].setdefault(sheet, 'All good!')
            else:
                report['disapproved'].setdefault(sheet, 'WARNING! Missing!')

        ValidatorLog.update_info(
            delivery_file_name=self.delivery_file_name,
            validator_name=self.name,
            info=report,
        )
