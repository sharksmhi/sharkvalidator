# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).
"""
Created on 2020-12-15 14:00

@author: johannes
"""
from abc import ABC


class WriterBase(ABC):
    """Base Class for writers."""

    def __init__(self, *args, **kwargs):
        """Initialize."""
        self.sheet_name = None
        self.na_rep = None
        self.index = None
        self.encoding = None
        for key, item in kwargs.items():
            setattr(self, key, item)

    def write(self, *args, **kwargs):
        """Write."""
        raise NotImplementedError

    def _write(self, *args, **kwargs):
        """Write."""
        raise NotImplementedError
