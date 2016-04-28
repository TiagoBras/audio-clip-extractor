# -*- coding: utf-8 -*-
from .core import AudioClipExtractor

from .parser import SpecsParser, AudioClipSpec

__all__ = [
    # Core
    'AudioClipExtractor',

    # Udacity parser
    'SpecsParser', 'AudioClipSpec'
]
