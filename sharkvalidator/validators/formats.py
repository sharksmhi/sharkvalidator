# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
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
from sharkvalidator.utils import get_app_directory, CodeDict, floatable
from sharkvalidator.validators.validator import Validator, ValidatorLog


class FormatValidator(Validator):
    """
    Node class for format validators.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, item in kwargs.items():
            setattr(self, key, item)

    def validate(self, delivery, disapproved_only=None, **kwargs):
        """"""
        if not hasattr(self, 'format_validators'):
            raise AttributeError('Missing "format_validators" as attribute! Please check your validator settings file')
        if not hasattr(self, 'parameters'):
            raise AttributeError('Missing "parameters" as attribute! Please check your validator settings file')

        # print('Validating: {}'.format(self.__class__.__name__))

        report = {'disapproved': {}} if disapproved_only else {'approved': {}, 'disapproved': {}}

        for key, item in self.format_validators.items():
            if isinstance(item, dict):
                validator = item.get('validator')
                self.format_validators[key] = validator(**{k: i for k, i in item.items() if k != 'validator'})

        for parameter, item in self.parameters.items():
            validator = self.format_validators.get(item.get('format_validator'))
            if validator:
                validator.update_attributes(**{k: i for k, i in item.items() if k != 'format_validator'})
            else:
                continue

            for element, df in delivery.items():
                if parameter in df:
                    print(df)
                    print(parameter)
                    print(df[parameter])
                    validation_result = validator.validate(df[parameter])
                    if validation_result.get('validation'):
                        report_key = ' - '.join((element, parameter))
                        if validation_result.get('approved'):
                            if not disapproved_only:
                                report['approved'].setdefault(report_key, 'Format OK!')
                        else:
                            report['disapproved'].setdefault(report_key, validation_result.get('text'))

        ValidatorLog.update_info(
            delivery_name=delivery.name,
            validator_name=self.name,
            info=report,
        )


class CodeValidator(Validator):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, item in kwargs.items():
            setattr(self, key, item)

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
        """"""
        s = set()
        for string in values:
            s |= set(v.strip() for v in string.split(','))
        return s

    def validate(self, serie, **kwargs):
        """"""
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
                codes = (True if c in valid_codes else False for c in self.unique_values(serie[boolean].unique()))
                if not all(codes):
                    result['approved'] = False
                    result['text'] = 'Codes are inconsistent with standard code format of {}'\
                        .format(self.code_list.mapper.get(serie.name, serie.name))
            except ValueError:
                result['approved'] = False
                result['text'] = 'ValueError! string instead of interger or float values?'
        return result


class DateTimeValidator(Validator):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, item in kwargs.items():
            setattr(self, key, item)

    def validate(self, serie, **kwargs):
        """"""
        result = {
            'validation': False,
            'approved': True,
            'text': '',
        }
        boolean = serie.ne('')
        print(serie.name)
        print(boolean)
        if boolean.any():
            result['validation'] = True
            try:
                boolean = pd.to_datetime(serie[boolean], format=self.fmt, errors='coerce').notna()
                if not boolean.all():
                    result['approved'] = False
                    result['text'] = 'Values are inconsistent with standard format ({})'.format(self.fmt)
            except ValueError:
                result['approved'] = False
                result['text'] = 'ValueError! string instead of interger or float values?'
        return result


class FreeTextValidator(Validator):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, item in kwargs.items():
            setattr(self, key, item)

    def validate(self, serie, **kwargs):
        """"""
        result = {
            'validation': False,
            'approved': True,
            'text': '',
        }
        boolean = serie.ne('')
        if boolean.any():
            # TODO Anything?... at all?..no?.. allrighty then!
            result['validation'] = True
        return result


class PositionValidator(Validator):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, item in kwargs.items():
            setattr(self, key, item)

    def validate(self, serie, **kwargs):
        """"""
        result = {
            'validation': False,
            'approved': True,
            'text': '',
        }
        # TODO we probably want an API solution here..
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
                    result['text'] = 'Values outside range ({} - {})'.format(self.lower_range, self.upper_range)
            except ValueError:
                result['approved'] = False
                result['text'] = 'ValueError! string instead of interger or float values? ' \
                                 'or maybe decimal sign: comma instead of dot?'
        return result


class RangeValidator(Validator):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, item in kwargs.items():
            setattr(self, key, item)

    def validate(self, serie, **kwargs):
        """"""
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
                    result['text'] = 'Values outside range ({} - {})'.format(self.lower_range, self.upper_range)
            except ValueError:
                result['approved'] = False
                float_boolean = serie[boolean].apply(lambda x: floatable(x))
                unvalid_values = ', '.join(serie[boolean][~float_boolean].unique())
                result['text'] = 'ValueError! string instead of interger or float values? ' \
                                 'or maybe decimal sign: comma instead of dot? ' \
                                 'Look up the following values: {}'.format(unvalid_values)
        return result
