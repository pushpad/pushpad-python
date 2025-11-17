# -*- coding: utf-8 -*-
"""Public package interface."""

from ._version import __version__
from .exceptions import PushpadAPIError, PushpadClientError, PushpadError
from .pushpad import Pushpad

__all__ = [
    "__version__",
    "Pushpad",
    "PushpadError",
    "PushpadClientError",
    "PushpadAPIError",
]
