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
    _handle = 0
    _onEnd = None
    _played = False
    _stopped = False
    onEnd = None
    path = ''

    def __del__(self):
        """Free the resources used by Bass for this song when destroying it."""
        if not self._stopped:
            bass.BASS_StreamFree(self._handle)

    def __init__(self, path: str):
        """Open a music file and prepare it for playing.

        The path to the file is converted to UTF-16 on Windows and UTF-8 on
        other platforms, allowing non-ASCII file names. Bass uses the file
        contents to determine the file type, so inaccruate extensions are
        allowed.
        """
        self.path = path
        if adj.platform.os == 'windows' or adj.platform.os == 'cygwin':
            path = path.encode('UTF-16')[2:] + b'\x00'
            flags = StreamFlags.AUTOFREE | SampleFlags.FLOAT | UNICODE
        else:
            path = path.encode('UTF-8')
            flags = StreamFlags.AUTOFREE | SampleFlags.FLOAT
        self._handle = bass.BASS_StreamCreateFile(False, path, 0, 0, flags)
        if self._handle == 0:
            error = bass.BASS_ErrorGetCode()
            raise Errors.openFile[error][0](Errors.openFile[error][1])
        def callback(event, channel, arg, data):
            self._stopped = True
            if self.onEnd is not None:
                self.onEnd()
        self._onEnd = SyncCallback(callback)
        bass.BASS_ChannelSetSync(
            self._handle,
            SyncFlags.END | SyncFlags.ONETIME,
            0,
            self._onEnd,
            None
        )
        metadata = tags.TAGS_Read(
            self._handle,
            b'album\x1F%ALBM\x1E' \
            b'artist\x1F%ARTI\x1E' \
            b'title\x1F%TITL\x1E' \
            b'track\x1F%TRCK'
        ).decode('UTF-8').split('\x1E')
        metadata = dict(item.partition('\x1F')[::2] for item in metadata)
        metadata['track'] = metadata['track'].partition('/')[0]
        if metadata['track'].isnumeric():
            metadata['track'] = int(metadata['track'])
        self.metadata = metadata

    def __repr__(self):
        """Return what the constructor to create the object looked like."""
        return '{}.{}({})'.format(
            type(self).__module__,
            type(self).__name__,
            repr(self.path)
        )

    def _getState(self) -> ChannelActivities:
        if self._stopped:
            return ChannelActivities.STOPPED
        state = bass.BASS_ChannelIsActive(self._handle)
        if state == ChannelActivities.STOPPED:
            if self._played:
                self._stopped = True
                return ChannelActivities.STOPPED
            return ChannelActivities.PAUSED
        return ChannelActivities(state)

    def fade(self, time: float=1.0):
        """Fade out the song over some amount of seconds, stopping it.

        When the song finishes fading out, it is freed and considered stopped.
        This does not trigger the "onEnd" callback. If the song is paused, it
        is just stopped instead.
        """
        state = self._getState()
        if state == ChannelActivities.STOPPED:
            raise TypeError('this song has been stopped')
        if state == ChannelActivities.PLAYING:
            time = int(time * 1000)
            bass.BASS_ChannelSlideAttribute(
                self._handle,
                Attributes.VOL,
                -1,
                time
            )
        else:
            bass.BASS_ChannelStop(self._handle)
        self._stopped = True

    def pause(self):
        """Pause the song, allowing it to continue where it was paused."""
        if not self.playing:
            return
        bass.BASS_ChannelPause(self._handle)

    def play(self):
        """Play/resume the song."""
        if self.stopped:
            raise TypeError('this song has been stopped')
        if self.playing:
            return
        bass.BASS_ChannelPlay(self._handle, False)
        self._played = True

    @property
    def playing(self) -> bool:
        """Whether this song is currently playing."""
        return self._getState() == ChannelActivities.PLAYING

    def stop(self):
        """Stop playing this song and free its resources.

        Once stopped, the song cannot be started/resumed.
        """
        if self.stopped:
            return
        bass.BASS_ChannelStop(self._handle)
        self._stopped = True

    @property
    def stopped(self) -> bool:
        """Whether this song has stopped permanently.

        This is distinct from a song that is merely paused. Also, a song that
        has not started playing is not considered "stopped" unless the stop
        method was explicitly called.
        """
        return self._getState() == ChannelActivities.STOPPED


bass, tags = loadLib()
