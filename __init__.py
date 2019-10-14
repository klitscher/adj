"""Atmospheric DJ: play songs fitting your mood
Longer description
"""


import collections as _collections
import sys as _sys


_Platform = _collections.namedtuple('Platform', ('os', 'bits'))


def _getPlatform() -> _Platform:
    """Get the operating system and word size of the computer."""
    if _sys.platform.startswith('cygwin'):
        os = 'cygwin'
    elif _sys.platform.startswith('darwin'):
        os = 'mac'
    elif _sys.platform.startswith('win32'):
        os = 'windows'
    else:
        os = 'unix'
    if _sys.maxsize == 0x7FFFFFFF:
        bits = 32
    elif _sys.maxsize == 0x7FFFFFFFFFFFFFFF:
        bits = 64
    else:
        bits = -1
    return _Platform(os, bits)


path = __path__[0]
platform = _getPlatform()