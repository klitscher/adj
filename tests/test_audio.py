import adj
import adj.audio
import os
import os.path
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
