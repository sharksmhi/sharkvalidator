# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-12-15 14:00

@author: johannes
"""
from abc import ABC


class WriterBase(ABC):
    """Base Class for writers."""

    def __init__(self, *args, **kwargs):
        """Initialize."""
        super().__init__()

    def write(self, *args, **kwargs):
        """Write."""
        raise NotImplementedError

    def _write(self, *args, **kwargs):
        """Write."""
        raise NotImplementedError
