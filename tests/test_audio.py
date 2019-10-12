import adj
import adj.audio
import gc
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

    def testPlayPause(self):
        """Play and pause the song, making sure it resumes."""
        song = None
        for extension in ('mp3', 'ogg'):
            with self.subTest(extension):
                path = os.path.join(adj.path, 'tests', 'sample.' + extension)
                song = adj.audio.Music(path)
                song.play()
                time.sleep(.2)
                pos = adj.audio.bass.BASS_ChannelGetPosition(
                    song._handle,
                    adj.audio.PositionFlags.BYTE
                )
                self.assertGreater(pos, 0)
                song.pause()
                self.assertFalse(song.playing)
                song.play()
                time.sleep(.1)
                self.assertLess(pos, adj.audio.bass.BASS_ChannelGetPosition(
                    song._handle,
                    adj.audio.PositionFlags.BYTE
                ))
                self.assertTrue(song.playing)
                song.stop()
                self.assertFalse(song.playing)
                with self.assertRaises(TypeError):
                    song.play()
        if isinstance(song, adj.audio.Music): song.stop()

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

    def testUnicode(self):
        """Ensure audio files with Unicode names can play."""
        song = os.path.join(adj.path, 'tests', '앢⓫䖴ᦓᙴ.mp3')
        song = adj.audio.Music(song)
