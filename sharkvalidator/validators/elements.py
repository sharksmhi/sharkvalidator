# Copyright (c) 2021 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).
"""
Created on 2021-01-07 15:54

@author: johannes
"""
from sharkvalidator.validators.validator import Validator, ValidatorLog
from sharkvalidator.utils import deep_get


class ElementValidator(Validator):
    """Validator for elements in delivery.

    In order for this validation to pass we need all element of a
    delivery to be in place with the correct name.

    Example: A physical and chemical delivery
    should include the following excel sheets:
        - "Förklaring" (delivery_note)
        - "Kolumner" (data)
        - "Analysinfo" (analyse_info)
        - "Provtagningsinfo" (sampling_info)
    """

    def validate(self, delivery, disapproved_only=None, **kwargs):
        """Validate to see if delivery contains all mandatory "elements"."""
        report = {'disapproved': {}} if disapproved_only else {'approved': {}, 'disapproved': {}}

        element_list = deep_get(self.data_types, [delivery.data_type, 'element_list']) or []

        for element in element_list:
            if not delivery.__contains__(element):
                report['disapproved'].setdefault(element, 'Missing! Corrupt file?')
            elif delivery[element].empty:
                report['disapproved'].setdefault(element, 'Missing! or corrupted file?')
            else:
                if not disapproved_only:
                    report['approved'].setdefault(element, 'All good!')

        ValidatorLog.update_info(
            delivery_name=delivery.name,
            validator_name=self.name,
            info=report,
        )
