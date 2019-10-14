import adj
import adj.audio
import gc
import itertools
import os
import os.path
import threading
import time
import unittest


class AudioTests (unittest.TestCase):
    """Test the audio system."""

    @classmethod
    def setUpClass(cls):
        """Initialize the audio system."""
        card = int(os.getenv('ADJ_DEVICE', 0))
        adj.audio.init(card)

    @unittest.skipIf(
        os.getenv('ADJ_DEVICE', 0) == 0,
        'audio device not selected, skipping manual test'
    )
    def testAudible(self):
        """Try to play sound and prompt the tester if they hear it."""
        song = None
        for extension in ('mp3', 'ogg'):
            with self.subTest(extension):
                path = os.path.join(adj.path, 'tests', 'sample.' + extension)
                song = adj.audio.Music(path)
                song.play()
                answer = input('Is music playing? (y/n) ')
                while answer.lower() not in 'ny':
                    answer = input('Enter just "y" or "n".')
                song.stop()
                self.assertEqual(answer, 'y')
        if isinstance(song, adj.audio.Music): song.stop()

    def testPausePlay(self):
        """Ensure that the song resumes where it left off after pausing."""
        for extension in ('mp3', 'ogg'):
            with self.subTest(extension):
                song = os.path.join(adj.path, 'tests', 'sample.' + extension)
                song = adj.audio.Music(song)
                song.play()
                time.sleep(.2)
                pos = adj.audio.bass.BASS_ChannelGetPosition(
                    song._handle,
                    adj.audio.PositionFlags.BYTE
                )
                self.assertGreater(pos, 0)
                song.pause()
                song.play()
                time.sleep(.1)
                self.assertLess(pos, adj.audio.bass.BASS_ChannelGetPosition(
                    song._handle,
                    adj.audio.PositionFlags.BYTE
                ))
                song.stop()

    def testSongFreed(self):
        """Ensure the song's resources are freed as intended."""
        song = None
        for extension, length in (('mp3', 6961528), ('ogg', 19033400)):
            with self.subTest(extension):
                path = os.path.join(adj.path, 'tests', 'sample.' + extension)
                with self.subTest('free on end'):
                    song = adj.audio.Music(path)
                    lock = threading.Lock()
                    lock.acquire()
                    @adj.audio.SyncCallback
                    def callback(a, b, c, d):
                        lock.release()
                    adj.audio.bass.BASS_ChannelSetSync(
                        song._handle,
                        adj.audio.SyncFlags.FREE,
                        0,
                        callback,
                        None
                    )
                    song.play()
                    adj.audio.bass.BASS_ChannelSetPosition(
                        song._handle,
                        length - 1,
                        (
                            adj.audio.PositionFlags.BYTE |
                            adj.audio.PositionFlags.SCAN |
                            adj.audio.PositionFlags.INEXACT
                        )
                    )
                    self.assertTrue(lock.acquire(timeout=2))
                with self.subTest('free on stop'):
                    song = adj.audio.Music(path)
                    song.stop()
                    adj.audio.bass.BASS_ChannelGetLength(song._handle, 0)
                    self.assertEqual(
                        adj.audio.bass.BASS_ErrorGetCode(),
                        adj.audio.Errors.HANDLE
                    )
                if isinstance(song, adj.audio.Music): song.stop()
                with self.subTest('free on garbage collection'):
                    song = adj.audio.Music(path)
                    handle = song._handle
                    del song
                    gc.collect()
                    adj.audio.bass.BASS_ChannelGetLength(handle, 0)
                    self.assertEqual(
                        adj.audio.bass.BASS_ErrorGetCode(),
                        adj.audio.Errors.HANDLE
                    )

    def testStartStop(self):
        """Start, stop, fade out, and pause the song in every permutation."""
        for extension in ('mp3', 'ogg'):
            with self.subTest(extension):
                path = os.path.join(adj.path, 'tests', 'sample.' + extension)
                methods = ('fade', 'pause', 'play', 'stop')
                methods = itertools.permutations(methods)
                for order in methods:
                    song = adj.audio.Music(path)
                    order = (getattr(song, method) for method in order)
                    stopped = False
                    for method in order:
                        if stopped and method in (song.fade, song.play):
                            with self.assertRaises(TypeError):
                                method()
                        else:
                            method()
                        if method in (song.fade, song.stop):
                            stopped = True
                        if not stopped and method == song.play:
                            self.assertTrue(song.playing)
                            self.assertFalse(song.stopped)
                        elif stopped:
                            self.assertFalse(song.playing)
                            self.assertTrue(song.stopped)
                        else:
                            self.assertFalse(song.playing)
                            self.assertFalse(song.stopped)
        if isinstance(song, adj.audio.Music): song.stop()

    def testUnicode(self):
        """Ensure audio files with Unicode names can play."""
        song = os.path.join(adj.path, 'tests', '앢⓫䖴ᦓᙴ.mp3')
        song = adj.audio.Music(song)
        song.stop()
