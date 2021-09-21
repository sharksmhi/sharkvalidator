# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-12-15 14:15

@author: johannes
"""
from pathlib import Path
from sharkvalidator.readers.xlsx import PandasXlsxReader
from sharkvalidator.readers.txt import PandasTxtReader


class PhysicalChemicalExcelReader(PandasXlsxReader):
    """Reader for the PhysicalChemical datatype."""

    def __init__(self, *args, **kwargs):
        """Initialize."""
        super().__init__(*args, **kwargs)


class PhysicalChemicalLIMSReader(PandasTxtReader):
    """Reader for the PhysicalChemical datatype acording to LIMS format."""

    def __init__(self, *args, **kwargs):
        """Initialize."""
        super().__init__(*args, **kwargs)
        self.arguments = list(args)
        self.files = {}

    def load(self, *args, **kwargs):
        """Activate files."""
        self._activate_files(*args, **kwargs)

    def read_element(self, *args, **kwargs):
        """Read data element.

        Reading excel sheet into pandas.Dataframe.
        """
        return self._read_file(*args, **kwargs)

    def _read_file(self, *args, **kwargs):
        """Read file (element) and return dataframe."""
        fid = args[0] if type(args) == tuple else args
        if fid in self.files:
            if kwargs.get('dtype') == '':
                kwargs['dtype'] = str
            df = self.read(self.files.get(fid), **kwargs)
            df = self.eliminate_empty_rows(df)
            df = self._move_qflags_from_data_cells(df)
        else:
            df = None
            print('File {} not found in delivery'.format(fid))
        return df

    def _move_qflags_from_data_cells(self, df):
        """Move Q-flags.

        Quality flags in LIMS-exoprt are stored within the data fields,
        therefor we need to move these q-flags from the data field into
        the Q-flag fields.

        Example: TEMP_CTD-value = 'B38.4' ---> '38.4' and Q_TEMP_CTD-value = 'B'
        """
        qflags = {'<', '>', 'B', 'S', 'E', 'M'}
        for key in self.data_columns:
            if key in df:
                for qf in qflags:
                    boolean = df[key].str.contains(qf, regex=False)
                    if boolean.any():
                        df.loc[boolean, key] = df.loc[boolean, key].str.replace(qf, '')
                        df.loc[boolean, 'Q_' + key] = qf
        return df

    def _activate_files(self, *args, **kwargs):
        """Set folder paths to self.files."""
        folder_path = Path(args[0]) if type(args) == tuple else Path(args)
        if not folder_path.exists:
            raise FileNotFoundError('Could not find the given LIMS-directory: {}'.format(folder_path))
        if folder_path.name != 'Raw_data':
            folder_path = folder_path / 'Raw_data'

        for file_name in folder_path.glob('**/*'):
            self.files.setdefault(file_name.name, file_name)
