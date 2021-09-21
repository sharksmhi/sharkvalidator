# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-12-16 13:52

@author: johannes

format_validators:
    code:
        validator: !!python/name:sharkvalidator.validators.formats.CodeValidator ''
    date:
        validator: !!python/name:sharkvalidator.validators.formats.DateValidator ''
        fmt: '%Y-%m-%d'
    position:
        validator: !!python/name:sharkvalidator.validators.formats.PositionValidator ''
    range:
        validator: !!python/name:sharkvalidator.validators.formats.RangeValidator ''
    time:
        validator: !!python/name:sharkvalidator.validators.formats.TimeValidator ''
        fmt: '%H:%M'

parameters:
    MYEAR:
        format_validator: date
        fmt: '%Y'
"""
import os
import pandas as pd
from sharkvalidator.utils import (
    get_app_directory,
    CodeDict,
    floatable,
)
from sharkvalidator.handler import Frame
from sharkvalidator.validators.validator import Validator, ValidatorLog


def duplicate_result():
    """Return string on duplicated parameters."""
    return 'Duplicated parameters/fields in datafile'


class FormatValidator(Validator):
    """Node class for format validators.

    In order for these format validators to pass we need values for all
    parameters of the delivery to pass the given validator for the specific parameter.

    Example: A physical and chemical delivery may include values for
    numerous fields, some of them are:
        - PROJ (code validation)
        - LATIT/LONGI (position validation)
        - SDATE (datetime validation)
        - TEMP_CTD (range validation)
    """

    def validate(self, delivery, disapproved_only=None, **kwargs):
        """Validate data field formats.

        Args:
            delivery (dict): Delivery with its elements.
            disapproved_only (bool): If set to True the ValidatorLog will only
                                     include disapproved validation information.
            **kwargs:
        """
        if not hasattr(self, 'format_validators'):
            raise AttributeError(
                'Missing "format_validators" as attribute! '
                'Please check your validator settings file'
            )
        if not hasattr(self, 'parameters'):
            raise AttributeError(
                'Missing "parameters" as attribute! '
                'Please check your validator settings file'
            )

        if disapproved_only:
            report = {'disapproved': {}}
        else:
            report = {'approved': {}, 'disapproved': {}}

        # Initiate format validators (eg. CodeValidator, DateTimeValidator, etc).
        for key, item in self.format_validators.items():
            if isinstance(item, dict):
                validator = item.get('validator')
                self.format_validators[key] = validator(
                    **{k: i for k, i in item.items() if k != 'validator'}
                )

        # Each parameter is connected to a certain validator called "format_validator".
        for parameter, item in self.parameters.items():
            validator = self.format_validators.get(item.get('format_validator'))
            if validator:
                validator.update_attributes(
                    **{k: i for k, i in item.items() if k != 'format_validator'}
                )
            else:
                # No validator, jump to next loop iteration (next parameter).
                # TODO: Raise Warning?
                continue

            # Validator exsits.
            for element, df in delivery.items():
                if parameter in df:
                    if type(df[parameter]) == Frame:
                        # TODO should probably move this to a seperate validator.
                        #  Not quite sur about when/why this condition becomes true.
                        #  Concerning duplicate parameters (?).
                        duplicate_text = duplicate_result()
                        report_key = ' - '.join((element, parameter))
                        report['disapproved'].setdefault(report_key, duplicate_text)
                        continue

                    # Validate field.
                    validation_result = validator.validate(df[parameter])

                    if validation_result.get('validation'):
                        report_key = ' - '.join((element, parameter))
                        if validation_result.get('approved'):
                            if not disapproved_only:
                                report['approved'].setdefault(
                                    report_key,
                                    'Format OK!'
                                )
                        else:
                            report['disapproved'].setdefault(
                                report_key,
                                validation_result.get('text')
                            )

        # Report validation information to log.
        ValidatorLog.update_info(
            delivery_name=delivery.name,
            validator_name=self.name,
            info=report,
        )


class CodeValidator(Validator):
    """Validator for codes."""

    def __init__(self, *args, **kwargs):
        """Initialize and set attributes from kwargs."""
        super().__init__(*args, **kwargs)

        # TODO we probably want an API solution here..
        cl = pd.read_excel(
            os.path.join(get_app_directory(), self.path_to_codelist),
            sheet_name="codelist_SMHI",
            header=1,
            dtype=str,
            keep_default_na=False,
        )
        self.code_list = CodeDict()
        for attr in cl['Data_field'].unique():
            boolean = cl['Data_field'] == attr
            set_with_values = set(cl.loc[boolean, 'Code'].values)
            if attr in ['DTYPE', 'LABO', 'PROJ', 'MATRX', 'METCU',
                        'METFP', 'METOA', 'METST', 'MPROG', 'MSTAT',
                        'MUNIT', 'NTYPE', 'OBSPOINT', 'PARAM', 'PDMET',
                        'POSYS', 'PURPM', 'REFSK', 'RLIST', 'SEXCODE',
                        'SFLAG', 'SIZRF', 'SMTYP', 'SPLIT', 'STAGE', 'STRID',
                        'SUBST', 'TALGAE', 'TRPHY', 'WLTYP']:
                set_with_values |= set(cl.loc[boolean, 'Beskrivning/Svensk översättning'].values)
                set_with_values |= set(cl.loc[boolean, 'Description/English translate'].values)

            self.code_list.setdefault_values(attr, set_with_values)

    @staticmethod
    def unique_values(values):
        """Return set of values."""
        s = set()
        for string in values:
            s |= set(v.strip() for v in string.split(','))
        return s

    def validate(self, serie, **kwargs):
        """Validate codes in serie."""
        result = {
            'validation': False,
            'approved': True,
            'text': '',
        }
        boolean = serie.ne('')
        if boolean.any():
            result['validation'] = True
            try:
                valid_codes = self.code_list.map_get(serie.name)
                codes = set()
                for value in self.unique_values(serie[boolean].unique()):
                    codes |= set(v.strip() for v in value.split(','))
                code_boolean = [True if c in valid_codes else False for c in codes]
                if not all(code_boolean):
                    result['approved'] = False
                    unvalid_values = ', '.join(
                        (c for c, bol in zip(codes, code_boolean) if not bol)
                    )
                    result['text'] = 'Codes are inconsistent with standard code format of {}. ' \
                                     'Look up the following values: {}'.format(
                        self.code_list.mapper.get(serie.name, serie.name),
                        unvalid_values
                    )
            except ValueError:
                result['approved'] = False
                result['text'] = 'ValueError! string instead of interger or float values?'
        return result


class DateTimeValidator(Validator):
    """Validator for DateTime formats."""

    def validate(self, serie, **kwargs):
        """Validate date/time values in serie."""
        result = {
            'validation': False,
            'approved': True,
            'text': '',
        }
        boolean = serie.ne('')
        if boolean.any():
            result['validation'] = True
            try:
                boolean = pd.to_datetime(serie[boolean], format=self.fmt, errors='coerce').notna()
                if not boolean.all():
                    result['approved'] = False
                    result['text'] = 'Values are inconsistent with standard format ({})'\
                        .format(self.fmt)
            except ValueError:
                result['approved'] = False
                result['text'] = 'ValueError! string instead of interger or float values?'
        return result


class FreeTextValidator(Validator):
    """Validator for text formats."""

    def validate(self, serie, **kwargs):
        """Validate text values in serie."""
        result = {
            'validation': False,
            'approved': True,
            'text': '',
        }
        boolean = serie.ne('')
        if boolean.any():
            # TODO Anything?... at all?..no?.. allrighty then!
            #  So, this check can never fail? why the fuss then?
            result['validation'] = True
        return result


class PositionValidator(Validator):
    """Validator for position formats."""

    def validate(self, serie, **kwargs):
        """Validate position values in serie."""
        result = {
            'validation': False,
            'approved': True,
            'text': '',
        }
        # TODO we probably want an microservice solution here..
        # Check aginst shapefile?
        boolean = serie.ne('')
        if boolean.any():
            result['validation'] = True
            try:
                float_serie = serie[boolean].astype(float)
                boolean = float_serie >= self.lower_range
                boolean = boolean & (float_serie <= self.upper_range)
                if not boolean.all():
                    result['approved'] = False
                    result['text'] = 'Values outside range ({} - {})'\
                        .format(self.lower_range, self.upper_range)
            except ValueError:
                result['approved'] = False
                result['text'] = 'ValueError! string instead of interger or float values? ' \
                                 'or maybe decimal sign: comma instead of dot?'
        return result


class RangeValidator(Validator):
    """Validator for range formats."""

    def validate(self, serie, **kwargs):
        """Validate to see if values lies within the given range."""
        result = {
            'validation': False,
            'approved': True,
            'text': '',
        }
        boolean = serie.ne('')
        if boolean.any():
            result['validation'] = True
            try:
                float_serie = serie[boolean].astype(float)
                boolean = float_serie >= self.lower_range
                boolean = boolean & (float_serie <= self.upper_range)
                if not boolean.all():
                    result['approved'] = False
                    result['text'] = 'Values outside range ({} - {})'\
                        .format(self.lower_range, self.upper_range)
            except ValueError:
                result['approved'] = False
                float_boolean = serie[boolean].apply(lambda x: floatable(x))
                unvalid_values = ', '.join(serie[boolean][~float_boolean].unique())
                result['text'] = 'ValueError! string instead of interger or float values? ' \
                                 'or maybe decimal sign: comma instead of dot? ' \
                                 'Look up the following values: {}'.format(unvalid_values)
        return result
