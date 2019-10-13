"""Manage the playing of audible sound on the computer.

This module depends entirely on the proprietary Bass library, since I couldn't
find a Python package that worked well enough across platforms. However, since
the library is a compiled object file, it's a little difficult to use directly.
This module's job is to provide a high-level interface to Bass's functions.
"""

import adj
from adj.basslib import *
import collections.abc
import itertools
import typing


def enumerateDevices() -> typing.List[SoundCardInfo]:
    """Get a list of output devices attached to the computer."""
    ret = []
    for i in itertools.count():
        card = SoundCardInfo()
        if bass.BASS_GetDeviceInfo(i, card):
            ret.append(card)
        else:
            return ret


def init(card: int=-1) -> ctypes.CDLL:
    """Initialize the audio system.

    The first argument is the index of the sound output device, but using -1
    will initialize the default device.
    """
    if not bass.BASS_Init(card, 48000, 0, None, None):
        error = bass.BASS_ErrorGetCode()
        raise Errors.init[error][0](Errors.init[error][1])


class Music:
    """A music file hooked up to the computer's sound hardware.

    Music objects support only playing, pausing, and stopping, since the
    application demands nothing more. However, since this object holds an open
    file and some additional resources in Bass, you should call the stop
    method explicitly when done playing to avoid leaking.
    """
    _callback = None
    _handle = 0
    path = ''

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
        self.path = path
        if adj.platform.os == 'windows' or adj.platform.os == 'cygwin':
            path = path.encode('UTF-16')[2:]
            flags = StreamFlags.AUTOFREE | SampleFlags.FLOAT | UNICODE
        else:
            path = path.encode('UTF-8')
            flags = StreamFlags.AUTOFREE | SampleFlags.FLOAT
        self._handle = bass.BASS_StreamCreateFile(False, path, 0, 0, flags)
        if self._handle == 0:
            error = bass.BASS_ErrorGetCode()
            raise Errors.openFile[error][0](Errors.openFile[error][1])

    def __repr__(self):
        """Return what the constructor to create the object looked like."""
        return '{}.{}({})'.format(
            type(self).__module__,
            type(self).__name__,
            repr(self.path)
        )
        
    def onEnd(self, function: collections.abc.Callable):
        """Register callback to be called when the song reaches the end.
        
        Only one callback can be set per Music object. If you call this twice,
        the first callback will be unset and replaced with the new one. It's
        recommended to call this method only before the song starts playing
        to guarantee no race condition. The callback is also removed by Bass
        once it runs."""
        if self._callback is not None:
            bass.BASS_ChannelRemoveSync(self._handle, self._callback.handle)
        def callback(event, song, _, obj):
            self._callback = None
            function(self)
        self._callback = SyncCallback(callback)
        self._callback.handle = bass.BASS_ChannelSetSync(
            self._handle,
            SyncFlags.END | SyncFlags.ONETIME,
            0,
            self._callback,
            None
        )

    def pause(self):
        """Pause the song, allowing it to continue where it was paused."""
        if not self.playing:
            return
        bass.BASS_ChannelPause(self._handle)

    def play(self):
        """Play/resume the song."""
        if self._handle == 0:
            raise TypeError('this song has been stopped')
        if self.playing:
            return
        bass.BASS_ChannelPlay(self._handle, False)

    @property
    def playing(self):
        """Whether this song is currently playing."""
        result = bass.BASS_ChannelIsActive(self._handle)
        return result == ChannelActivities.PLAYING

    def stop(self):
        """Stop playing this song and free its resources.

        Once stopped, the song cannot be started/resumed.
        """
        bass.BASS_ChannelStop(self._handle)
        bass.BASS_StreamFree(self._handle)
        self._handle = 0


bass = loadLib()
