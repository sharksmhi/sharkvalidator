# Copyright (c) 2021 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-01-07 15:54

@author: johannes

"""
from sharkvalidator.validators.validator import Validator, ValidatorLog


class ElementValidator(Validator):
    """
    """
    def __init__(self, *args, **kwargs):
        super(ElementValidator, self).__init__(*args, **kwargs)
        for key, item in kwargs.items():
            setattr(self, key, item)

    def validate(self, *args, **kwargs):
        """"""
        assert self.element_list

        report = {'approved': {},
                  'disapproved': {}}

        for element in self.element_list:
            if element in self.reader.file.sheet_names:
                report['approved'].setdefault(sheet, 'All good!')
            else:
                report['disapproved'].setdefault(sheet, 'WARNING! Missing!')

        ValidatorLog.update_info(
            delivery_file_name=self.delivery_file_name,
            validator_name=self.name,
            info=report,
        )
