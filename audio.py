"""Manage the playing of audible sound on the computer.

This module depends entirely on the proprietary Bass library, since I couldn't
find a Python package that worked well enough across platforms. However, since
the library is a compiled object file, it's a little difficult to use directly.
This module's job is to provide a high-level interface to Bass's functions.
"""

import ctypes
import collections
import adj
import enum
import os.path
import sys


@enum.unique
class BassErrors (enum.IntEnum):
    """Enumeration of error codes documented by the Bass library."""
    OK = 0
    MEM = 1
    FILEOPEN = 2
    DRIVER = 3
    BUFLOST = 4
    HANDLE = 5
    FORMAT = 6
    POSITION = 7
    INIT = 8
    START = 9
    SSL = 10
    ALREADY = 14
    NOCHAN = 18
    ILLTYPE = 19
    ILLPARAM = 20
    NO3D = 21
    NOEAX = 22
    DEVICE = 23
    NOPLAY = 24
    FREQ = 25
    NOTFILE = 27
    NOHW = 29
    EMPTY = 31
    NONET = 32
    CREATE = 33
    NO_FX = 34
    NOTAVAIL = 37
    DECODE = 38
    DX = 39
    TIMEOUT = 40
    FILEFORM = 41
    SPEAKER = 42
    VERSION = 43
    CODEC = 44
    ENDED = 45
    BUSY = 46
    UNKNOWN = -1

BassErrors.init = collections.defaultdict(lambda: (Exception, 'unknown'), {
    BassErrors.DX: (OSError, 'no Bass-compatible audio driver installed'),
    BassErrors.DEVICE: (ValueError, 'invalid sound card index number'),
    BassErrors.ALREADY: (TypeError, 'Bass is already initialized'),
    BassErrors.DRIVER: (OSError, 'no available driver'),
    BassErrors.BUSY: (OSError, 'something else has control of the sound card'),
    BassErrors.FORMAT: (OSError, 'specified frequency not supported'),
    BassErrors.MEM: (MemoryError, 'out of memory initializing Bass')
})

BassErrors.openFile = collections.defaultdict(lambda: (Exception, 'unknown'), {
    BassErrors.INIT: (TypeError, 'Bass has not been initialized'),
    BassErrors.FILEOPEN: (OSError, 'could not open music file'),
    BassErrors.FILEFORM: (ValueError, 'music file format not recognized'),
    BassErrors.CODEC: (TypeError, 'no codec installed for music file'),
    BassErrors.FORMAT: (TypeError, 'unsupported sample format in music file'),
    BassErrors.MEM: (MemoryError, 'out of memory opening music file'),
})


def init(card: int=-1) -> ctypes.CDLL:
    """Initialize the audio system.

    This function is called when this module is imported and returns the
    imported Bass library. The first argument is the index of the sound output
    device, but using -1 will initialize the default device.
    """
    if adj.platform.os == 'cygwin':
        bass = ctypes.CDLL(os.path.join(adj.path, 'bass.dll'))
    elif adj.platform.os == 'mac':
        bass = ctypes.CDLL(os.path.join(adj.path, 'libbass.dynlib'))
    elif adj.platform.os == 'windows':
        bass = ctypes.WinDLL(os.path.join(adj.path, 'bass.dll'))
    else:
        bass = ctypes.CDLL(os.path.join(adj.path, 'libbass.so'))
    if not bass.BASS_Init(card, 48000, 0, 0, None):
        error = bass.BASS_ErrorGetCode()
        raise BassErrors.init[error][0](BassErrors.init[error][1])
    return bass


class Music:
    """A music file hooked up to the computer's sound hardware.

    Music objects support only playing, pausing, and stopping, since the
    application demands nothing more. However, since this object holds an open
    file and some additional resources in Bass, you should call the stop
    method explicitly when done playing to avoid leaking.
    """
    _handle = 0
    playing = False

    def __del__(self):
        """Free the resources used by Bass for this song when destroying it."""
        if self._handle != 0:
            bass.BASS_StreamFree(self._handle)
            self._handle = 0

    def __init__(self, path: str):
        """Open a music file and prepare it for playing.

        The path to the file is converted to UTF-16 on Windows and UTF-8 on
        other platforms, allowing non-ASCII file names. Bass uses the file
        contents to determine the file type, so inaccruate extensions are
        allowed.
        """
        if adj.platform.os == 'windows' or dj.platform.os == 'cygwin':
            path = path.encode('UTF-16')[2:]
            utf16 = 0x80000000
        else:
            path = path.encode('UTF-8')
            utf16 = 0
        self._handle = bass.BASS_StreamCreateFile(False, path, 0, 0, utf16)
        if self._handle == 0:
            error = bass.BASS_ErrorGetCode()
            raise BassErrors.openFile[error][0](BassErrors.openFile[error][1])
        self.playing = False

    def pause(self):
        """Pause the song, allowing it to continue where it was paused."""
        if not self.playing:
            return
        bass.BASS_ChannelPause(self._handle)
        self.playing = False

    def play(self):
        """Play/resume the song."""
        if self._handle == 0:
            raise TypeError('this song has been stopped')
        if self.playing:
            return
        bass.BASS_ChannelPlay(self._handle, False)
        self.playing = True

    def stop(self):
        """Stop playing this song and free its resources.

        Once stopped, the song cannot be started/resumed.
        """
        bass.BASS_ChannelStop(self._handle)
        bass.BASS_StreamFree(self._handle)
        self._handle = 0
        self.playing = False


bass = init()
