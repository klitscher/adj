#!usr/bin/env python3
"""Module that parses list of Albums and moods"""

def parseAlbumList(filePath):
    """Method to parse the album text file

    filePath: Path to the text file

    """
    albums = {}
    tracks = {}
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
