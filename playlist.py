import adj.audio
import adj.db
import collections
import collections.abc
import random


class Playlist (list):
    _random = random.Random()
    channel = None
    index = 0

    def __delitem__(self, key):
        if isinstance(key, slice):
            raise NotImplementedError('slice deletion not supported')
        super().__delitem__(key)
        if key == self.index or self.__len__() + key == self.index:
            self.next()
        if 0 <= key <= self.index:
            self.index -= 1
        if 0 > key <= self.index - self.__len__():
            self.index -= 1

    def __init__(self, iterable: collections.abc.Iterable=[], *, seed=None):
        """Construct a new playlist given an iterable of paths to music files.

        The optional seed argument determines the random.Random.seed value used
        to shuffle the playlist items."""
        super().__init__(iterable)
        self._random.seed(seed)
        self._random.shuffle(self)
        self.index = 0
        if self.__len__() > 0:
            self.channel = adj.audio.Music(self[0].path)
            self.channel.onEnd = self.next

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            raise NotImplementedError('slice assignment not implemented')
        super().__setitem__(key, value)
        if key == self.index or self.__len__() + key == self.index:
            if self.channel is not None:
                self.channel.stop()
                self.channel = adj.audio.Music(self[self.index].path)
                self.channel.onEnd = self.next

    def append(self, song):
        """Add one song to the end of the playlist."""
        super().append(song)
        if self.channel is None:
            self.channel = adj.audio.Music(self[-1].path)
            self.channel.onEnd = self.next

    def clear(self):
        """Empty the playlist, stopping any playing song."""
        super().clear()
        self.index = 0
        if self.channel is not None:
            self.channel.stop()
            self.channel = None

    def copy(self):
        """Return a shallow copy of the playlist."""
        return Playlist(super().copy())

    def extend(self, iterable):
        """Add the songs from iterable to the end of this playlist."""
        length = self.__len__()
        super().extend(iterable)
        if self.channel is None and self.__len__() > 0:
            self.channel = adj.audio.Music(self[length - 1].path)
            self.channel.onEnd = self.next

    def next(self, fadeOutTime=3.0, fadeInTime=2.0):
        """Skip to the next song in the playlist.

        The current song, if any, is stopped before moving to the next one. If
        there are no more songs in the playlist, this method does not play one.
        """
        playing = self.channel.playing
        if playing:
            self.channel.fadeOut(fadeOutTime)
        else:
            self.channel.stop()
        self.index = min(self.index + 1, self.__len__())
        if self.index < self.__len__():
            self.channel = adj.audio.Music(self[self.index].path)
            self.channel.onEnd = self.next
            if playing:
                self.channel.fadeIn(fadeInTime)
        elif self.__len__() == 0:
            self.channel = None

    def reverse(self):
        """Reverse the order of the playlist.

        The current position in the playlist is preserved and the current
        song keeps playing / remains paused.
        """
        super().reverse()
        self.index = self.__len__() - self.index - 1

    def pop(self, key=-1):
        """Remove a song from the playlist and return it.

        If the current song is removed, the playlist skips to the next one.
        Otherwise, the playlist index accounts for the change in size.
        """
        return super().pop(key)
        if key == self.index or self.__len__() + key == self.index:
            self.next()
        if 0 <= key <= self.index:
            self.index -= 1
        if 0 > key <= self.index - self.__len__():
            self.index -= 1
