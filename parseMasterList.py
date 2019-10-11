"""Module that parses list of Albums and moods"""

import re
import unicodedata


normalizer = re.compile(r'''
    ^\s*the\s+ |                 # remove "the" when it is the first word
    (?<=\w)\.(?=\s) |            # remove trailing dots on words (like "Mr.")
    \s*\((?!\)) | (?<!\()\) |    # remove parentheses around words
    \s*\bsoundtrack\b\s* |       # remove "soundtrack"
    \s*\boriginal\s+soundtrack\b\s*
''', re.VERBOSE)

def normalizeAlbum(name: str):
    """Remove extraneous text from an album name to make it easier to compare.

    Common words and most punctuation are removed. This helps users with
    unusually-tagged downloads match up with everyone else. It also helps
    oddly-tagged albums: for example, half of the Witcher 3 soundtrack is
    called "The Witcher 3: Wild Hunt" and the other half is the same but ends
    with "(Sountrack)".
    """

    name = unicodedata.normalize('NFKC', name)
    name = name.lower()
    name = re.sub(normalizer, '', name)
    name = re.sub('\\s+', ' ', name)
    name = name.strip()
    return name


def parseMasterList(filePath):
    """Method to parse the album text file

    filePath: Path to the text file

    """
    albums = {}
    with open(filePath) as f:
        albumName = None
        for line in f:
            if albumName is None:
                albumName = line.rstrip('\n')
                albums[albumName] = {}
                tracks = albums[albumName]
            elif line == '%\n':
                albumName = None
            else:
                track = line.partition(' ')[0]
                moods = set(line.partition(' ')[2].rstrip('\n').split(', '))
                tracks[track] = moods
    return albums
