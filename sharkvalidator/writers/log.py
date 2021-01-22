# Copyright (c) 2021 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-01-08 13:37

@author: johannes

"""
import yaml
import json

from sharkvalidator.writers.writer import WriterBase
from sharkvalidator.validators.validator import ValidatorLog


class ValidationWriter(WriterBase):
    """
    """
    def __init__(self, *args, **kwargs):
        super(ValidationWriter, self).__init__(*args, **kwargs)
        for key, item in kwargs.items():
            setattr(self, key, item)

    @staticmethod
    def write(file_path, **kwargs):
        """
        :param file_path: str
        :param list_obj: stations.validators.ValidatorLog.log
        :return:
        """
        # with open(file_path, "w", encoding='cp1252') as file:
        #     json.dump(
        #         ValidatorLog.log,
        #         file,
        #         indent=4,
        #     )
        with open(file_path, 'w') as file:
            yaml.safe_dump(
                ValidatorLog.log,
                file,
                indent=4,
                default_flow_style=False,
            )