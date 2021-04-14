# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-04-13 15:40
@author: johannes
"""
from pathlib import Path
import zipfile
import pandas as pd
from sharkvalidator.readers.txt import PandasTxtReader


class BaseSHARK(PandasTxtReader):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arguments = list(args)
        self.file = None

    def load(self, *args, **kwargs):
        self._activate_file(*args, **kwargs)

    def read_element(self, *args, **kwargs):
        df = self._read_file(*args, **kwargs)
        if type(df) == pd.DataFrame:
            for col in ['sample_latitude_dm', 'sample_longitude_dm',
                        'Sample latitude(DM)', 'Sample longitude(DM)',
                        'Provets latitud(DM)', 'Provets longitud(DM)']:
                if col in df:
                    df[col] = df[col].str.replace(' ', '')
        return df

    def _activate_file(self, *args, **kwargs):
        raise NotImplementedError

    def _read_file(self, *args, **kwargs):
        raise NotImplementedError


class SharkwebReader(BaseSHARK):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _read_file(self, *args, **kwargs):
        if kwargs.get('dtype') == '':
            kwargs['dtype'] = str
        df = self.read(self.file, **kwargs)
        df = self.eliminate_empty_rows(df)
        return df

    def _activate_file(self, *args, **kwargs):
        folder_path = Path(args[0]) if type(args) == tuple else Path(args)
        if not folder_path.exists:
            raise FileNotFoundError('Could not find the given LIMS-directory: {}'.format(folder_path))
        self.file = folder_path


class SharkzipReader(BaseSHARK):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _read_file(self, *args, **kwargs):
        if not self.file:
            return None

        fid = args[0] if type(args) == tuple else args
        if fid in self.file.namelist():
            if kwargs.get('dtype') == '':
                kwargs['dtype'] = str
            try:
                df = self.read(self.file.open(fid), **kwargs)
                df = self.eliminate_empty_rows(df)
            except:
                df = None
                print('Activated zipfile contains unreadable file: {} from package: {}'.format(fid, Path(self.file.filename).name))
        else:
            df = None
            print('Activated zipfile does not contain file: {}'.format(fid))
        return df

    def _activate_file(self, *args, **kwargs):
        zip_path = Path(args[0]) if type(args) == tuple else Path(args)
        if not zip_path.exists:
            raise FileNotFoundError('Could not find the given ZIP-directory: {}'.format(zip_path))
        if not zip_path.name.startswith(self.files_startswith):
            raise ValueError('The given ZIP-directory does not follow the correct format ({}): {}'.format(self.files_startswith, zip_path))
        try:
            self.file = zipfile.ZipFile(zip_path)
        except zipfile.BadZipfile:
            self.file = None
            print('File is not a zip file: {}'.format(zip_path))
