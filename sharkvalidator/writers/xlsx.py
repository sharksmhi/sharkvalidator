#!/usr/bin/env python3
# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-10-08 11:26

@author: johannes
"""
import copy
import pandas as pd
from sharkvalidator.writers.writer import WriterBase
from sharkvalidator.validators.validator import ValidatorLog


class ExcelWriter(WriterBase):
    """Excel writer."""

    def write(self, file_path, exclude_approved_formats=False, **kwargs):
        """Write ValidatorLog.log to excel file.

        Args:
            file_path (str): Path to file
            exclude_approved_formats (bool): False | True.
                                             If True only disapproved tests will
                                             be included in the file.
        """
        log_copy = copy.deepcopy(ValidatorLog.log)
        if exclude_approved_formats:
            for key, item in log_copy.items():
                if 'formats' in item:
                    if not any(item['formats']['disapproved']):
                        del log_copy[key]

        out_dict = self.get_writer_format(log_copy)
        df = pd.DataFrame(out_dict)

        df.to_excel(
            file_path,
            sheet_name=self.sheet_name,
            na_rep=self.na_rep,
            index=self.index,
            encoding=self.encoding,
            **kwargs
        )

    @staticmethod
    def get_writer_format(data):
        """Return ValidatorLog.log in format likeable to this writer."""
        out_dict = {
            'delivery': [],
            'validator': [],
            'type': [],
            'field': [],
            'comnt': [],
        }
        for delivery, item in data.items():
            if 'elements' in item:
                for element, item_element in item['elements'].items():
                    if any(item_element) and element == 'disapproved':
                        for key_type, item_type in item_element.items():
                            out_dict['delivery'].append(delivery)
                            out_dict['validator'].append('elements')
                            out_dict['type'].append(key_type)
                            out_dict['field'].append('')
                            out_dict['comnt'].append(item_type)

            for validator in ('essentials', 'formats'):
                if validator in item:
                    for element, item_element in item[validator].items():
                        if any(item_element) and element == 'disapproved':
                            for key_type, item_type in item_element.items():
                                out_dict['delivery'].append(delivery)
                                out_dict['validator'].append(validator)
                                typ, field = key_type.split(' - ')
                                out_dict['type'].append(typ)
                                out_dict['field'].append(field)
                                out_dict['comnt'].append(item_type)
        return out_dict
