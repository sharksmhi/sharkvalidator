# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).
"""
Created on 2020-12-15 14:10

@author: johannes
"""
import os
import requests
from copy import deepcopy
from pathlib import Path
from sharkvalidator.readers.yml import yaml_reader
from sharkvalidator.utils import (
    generate_filepaths,
    get_app_directory,
    recursive_dict_update,
    TranslateHeader,
    TranslateParameters,
)


class Settings:
    """Class to hold information from etc settings files."""

    def __init__(self, *args, **kwargs):
        """Initialize."""
        TranslateHeader()
        TranslateParameters()
        self.default_attributes = None
        self.readers = {}
        self.writers = {}
        self.validators = {}

        self.base_directory = get_app_directory()
        etc_path = os.path.join(self.base_directory, 'etc')
        self._load_settings(etc_path)
        self._check_for_code_list(etc_path)

    def _load_settings(self, etc_path):
        """Load settings files.

        Loading all yaml files from etc directory.
        Special handling of readers and writers (see self.__setattr__())
        """
        paths = generate_filepaths(etc_path, pattern='.yaml')
        etc_data = {}
        for path in paths:
            data = yaml_reader(path)
            etc_data.setdefault(path, data)

        self.set_attributes(**etc_data)

    @staticmethod
    def _check_for_code_list(etc_path):
        """Check if codelist, if not download."""
        file_path = os.path.join(etc_path, 'codelist_SMHI.xlsx')
        if not os.path.exists(file_path):
            print('Could not find codelist. Trying to download it instead..')
            r = requests.get(
                'http://smhi.se/oceanografi/oce_info_data/shark_web/downloads/'
                'codelist_SMHI.xlsx', allow_redirects=True,
            )
            open(file_path, 'wb').write(r.content)
            print('Download completed! file saved here: {}'.format(file_path))

    def load_reader(self, reader):
        """Return reader instance."""
        reader_instance = self.readers[reader].get('reader')
        return reader_instance(**deepcopy(self.readers.get(reader)))

    def load_writer(self, writer):
        """Return writer instance."""
        writer_instance = self.writers[writer].get('writer')
        return writer_instance(**self.writers.get(writer))

    def load_validator(self, validator):
        """Return validator instance."""
        validator_instance = self.validators[validator].get('validator')
        return validator_instance(**self.validators.get(validator))

    @property
    def validators_sorted(self):
        """Return sorted list of validator names."""
        return sorted(self.validators)

    @property
    def list_of_readers(self):
        """Return list of readers names."""
        return list(self.readers)

    @property
    def list_of_writers(self):
        """Return list of writers names."""
        return list(self.writers)

    @property
    def list_of_validators(self):
        """Return list of validators names."""
        return list(self.validators)

    def get_export_file_path(self, file_path=None, file_name=None,
                             default_file_name=None, **kwargs):
        """Return path to export filename.

        Whenever there´s not an export path given by the user,
        we try to export elsewhere.
        """
        if file_path:
            if os.path.isdir(file_path):
                return file_path
            elif os.path.isdir(Path(file_path).parent):
                return file_path
            else:
                raise Warning('file_path given, but it´s not valid.')

        target_path = 'C:/shark_validation_export'
        if os.path.isdir('C:/'):
            if not os.path.isdir(target_path):
                os.mkdir(target_path)
        else:
            target_path = self.base_directory

        file_name = file_name or default_file_name

        return os.path.join(target_path, file_name)

    def __setattr__(self, name, value):
        """Define the setattr for object self.

        Special management of readers and writers.
        """
        if os.path.isfile(name):
            if isinstance(value, dict) and (
                    'readers' in name or
                    'writers' in name or
                    'validators' in name
            ):
                if 'readers' in name:
                    recursive_dict_update(self.readers,
                                          {Path(name).stem: value})
                elif 'writers' in name:
                    recursive_dict_update(self.writers,
                                          {Path(name).stem: value})
                else:
                    recursive_dict_update(self.validators,
                                          {Path(name).stem: value})
            else:
                super().__setattr__(Path(name).stem, value)
        elif name == 'attributes':
            super().__setattr__(name, self._get_attribute_dictionary(value))
        else:
            super().__setattr__(name, value)

    @staticmethod
    def _get_attribute_dictionary(settings_attributes):
        """Get dictionary with attributes."""
        d = {}
        for key, item in settings_attributes.items():
            if isinstance(item, str):
                d.setdefault(item, key)
            elif isinstance(item, list):
                for attrb in item:
                    d.setdefault(attrb, key)
            else:
                raise Warning('Type of item is nor str or list:', type(item))
        return d

    def set_attributes(self, **kwargs):
        """Set attributes to self."""
        for key, value in kwargs.items():
            setattr(self, key, value)
