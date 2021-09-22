# Copyright (c) 2021 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).
"""
Created on 2021-01-11 13:15

@author: johannes
"""
from sharkvalidator.validators.validator import Validator, ValidatorLog
from sharkvalidator.utils import deep_get


class EssentialValidator(Validator):
    """Validator for essentials fields.

    In order for this validation to pass we need values for all essentials of a
    delivery to be included in the delivery.

    Example: A physical and chemical delivery should include values for
    numerous fields, some of them are:
        - SDATE
        - STIME
        - STATN
        - LATIT
        - LONGI
        - DEPH
        - and many more..
    """

    def validate(self, delivery, disapproved_only=None, **kwargs):
        """Validate to see if dataframe contains all "essentials" fields."""
        if disapproved_only:
            report = {'disapproved': {}}
        else:
            report = {'approved': {}, 'disapproved': {}}

        for element, item in delivery.items():
            parameter_list = deep_get(self.data_types, [delivery.data_type, element]) or []

            for parameter in parameter_list:
                report_key = ' - '.join((element, parameter))
                if parameter in item:
                    if item[parameter].ne('').all():
                        # not equal to ''
                        if not disapproved_only:
                            report['approved'].setdefault(report_key, 'No missing values')
                    else:
                        report['disapproved'].setdefault(report_key, 'Missing values')
                else:
                    report['disapproved'].setdefault(report_key, 'Missing this parameter/column')

        ValidatorLog.update_info(
            delivery_name=delivery.name,
            validator_name=self.name,
            info=report,
        )
