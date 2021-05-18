# Copyright (c) 2021 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-01-08 13:37

@author: johannes

"""
import yaml

from sharkvalidator.writers.writer import WriterBase
from sharkvalidator.validators.validator import ValidatorLog


class ValidationWriter(WriterBase):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, item in kwargs.items():
            setattr(self, key, item)

    @staticmethod
    def write(file_path, exclude_approved_formats=False, **kwargs):
        log_copy = ValidatorLog.log.copy()
        if exclude_approved_formats:
            for key, item in log_copy.items():
                if 'formats' in item:
                    if not any(item['formats']['disapproved']):
                        del log_copy[key]

        with open(file_path, 'w') as file:
            yaml.safe_dump(
                log_copy,
                file,
                indent=4,
                width=120,
                default_flow_style=False,
            )
