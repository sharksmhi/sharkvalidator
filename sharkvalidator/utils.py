# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-12-15 14:10

@author: johannes

"""
import os
from copy import deepcopy
import numpy as np
from collections import Mapping
from datetime import datetime
from pyproj import Proj, CRS, transform
from decimal import Decimal, ROUND_HALF_UP
from sharkvalidator.readers.txt import text_reader


def get_app_directory():
    return os.path.dirname(os.path.realpath(__file__))


def deep_get(d, keys):
    if d is None:
        return None
    if not keys:
        return d
    return deep_get(d.get(keys[0]), keys[1:])


def floatable(x):
    try:
        float(x)
    except ValueError:
        return False
    return True


def decmin_to_decdeg(pos, string_type=True, decimals=4):
    """
    :param pos: str, Position in format DDMM.mm (Degrees + decimal minutes)
    :param string_type: As str?
    :param decimals: Number of decimals
    :return: Position in format DD.dddd (Decimal degrees)
    """
    pos = float(pos)

    output = np.floor(pos/100.) + (pos % 100)/60.
    output = round_value(output, nr_decimals=decimals)
    # output = "%.5f" % output
    if string_type:
        return output
    else:
        return float(output)


def decdeg_to_decmin(pos: (str, float), string_type=True, decimals=2) -> (str, float):
    """
    :param pos: Position in format DD.dddd (Decimal degrees)
    :param string_type: As str?
    :param decimals: Number of decimals
    :return: Position in format DDMM.mm(Degrees + decimal minutes)
    """
    pos = float(pos)
    deg = np.floor(pos)
    minute = pos % deg * 60.0
    if string_type:
        if decimals:
            output = ('%%2.%sf'.zfill(7) % decimals % (float(deg) * 100.0 + minute))
        else:
            output = (str(deg * 100.0 + minute))

        if output.index('.') == 3:
            output = '0' + output
    else:
        output = (deg * 100.0 + minute)
    return output


def generate_filepaths(directory: str, pattern=''):
    """
    :param directory: str, directory path
    :param pattern: str
    :return: generator
    """
    for path, subdir, fids in os.walk(directory):
        for f in fids:
            if pattern in f:
                yield os.path.abspath(os.path.join(path, f))


def get_now_time(fmt=None) -> str:
    """
    :param fmt: str, format to export datetime object
    :return:
    """
    fmt = fmt or '%Y-%m-%d %H:%M:%S'
    return datetime.now().strftime(fmt)


def recursive_dict_update(d: dict, u: dict) -> dict:
    """ Recursive dictionary update using
    Copied from:
        http://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
        via satpy
    """
    for k, v in u.items():
        if isinstance(v, Mapping):
            r = recursive_dict_update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


def round_value(value: (str, int, float), nr_decimals=2) -> str:
    """"""
    return str(Decimal(str(value)).quantize(Decimal('%%1.%sf' % nr_decimals % 1), rounding=ROUND_HALF_UP))


def transform_ref_system(lat=0.0, lon=0.0,
                         in_proj='EPSG:3006',  # SWEREF 99TM 1200
                         out_proj='EPSG:4326'):
    """
    Transform coordinates from one spatial reference system to another.
    in_proj is your current reference system
    out_proj is the reference system you want to transform to, default is EPSG:4326 = WGS84
    (Another good is EPSG:4258 = ETRS89 (Europe), almost the same as WGS84 (in Europe)
    and not always clear if coordinates are in WGS84 or ETRS89, but differs <1m.
    lat = latitude
    lon = longitude
    To find your EPSG check this website: http://spatialreference.org/ref/epsg/
    """
    o_proj = CRS(out_proj)
    i_proj = CRS(in_proj)

    x, y = transform(i_proj, o_proj, float(lon), float(lat), always_xy=True)

    return y, x


def delete_key_from_dict(dictionary, key):
    """
    Loops recursively over nested dictionaries.
    """
    for k, v in dictionary.items():
        if key in v:
            del v[key]
        if isinstance(v, dict):
            delete_key_from_dict(v, key)
    return dictionary


class CodeDict(dict):
    def __init__(self, seq=None, **kwargs):
        super().__init__(seq=None, **kwargs)
        self.mapper = {
            'ALABO': 'LABO',
            'RLABO': 'LABO',
            'SLABO': 'LABO',
            'ORDERER': 'LABO',
            'CURDIR': 'WINDIR',
            'REFSK_SMP': 'REFSK',
            'REFSK_ANA': 'REFSK',
            'ADD_SMP': 'DTYPE',
        }

    def map_get(self, item):
        if item.startswith('Q_'):
            return self.get('QFLAG')
        elif item.startswith('ACKR_'):
            return {'Y', 'N', 'Yes', 'No'}
        return self.get(self.mapper.get(item, item))

    def setdefault_values(self, k, default):
        if k == 'WINDIR' or k == 'CURDIR':
            default |= set(v for v in default)
            default |= set(v.zfill(2) for v in default)
            default |= set('0')
        self[k] = self[k] if k in self else default


class MappingDict(dict):
    def __init__(self, seq=None, **kwargs):
        super().__init__(seq=None, **kwargs)

    def setdefault_values(self, k, default):
        if k and default:
            self[k] = self[k] if k in self else default


class TranslateHeader:
    data = MappingDict()

    def __init__(self):
        df = text_reader(
            'pandas',
            r'C:\Arbetsmapp\config\translate_headers.txt',
            sep='\t',
            header=0,
            encoding='cp1252',
            dtype=str,
            keep_default_na=False,
        )
        for row in df.itertuples():
            self.data.setdefault_values(row.internal_key, row.short)
            self.data.setdefault_values(row.english, row.short)
            self.data.setdefault_values(row.swedish, row.short)
            self.data.setdefault_values(row.darwin_core, row.short)

    @classmethod
    def map_get(cls, key):
        return cls.data.get(key, key)


class TranslateParameters:
    data = MappingDict()

    def __init__(self):
        df = text_reader(
            'pandas',
            r'C:\Arbetsmapp\config\translate_parameters.txt',
            sep='\t',
            header=0,
            encoding='cp1252',
            dtype=str,
            keep_default_na=False,
        )
        for row in df.itertuples():
            if row.short_param_name:
                self.data.setdefault_values(row.english_param_name, row.short_param_name)
                self.data.setdefault_values(row.swedish_param_name, row.short_param_name)

    @classmethod
    def map_get(cls, key):
        return cls.data.get(key, key)


if __name__ == '__main__':
    TranslateParameters()
