import adj
import adj.audio
import adj.db
import adj.masterlist
import os
import re


def populateMusic(music_root, db_obj):
    """parse user music and store matching items in db"""

    path = os.path.join(adj.path, 'allmoods.txt')
    albums = adj.masterlist.parseMasterList(path)

    for dirpath, dirnames, filenames in os.walk(music_root):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            try:
                song = adj.audio.Music(path)
            except ValueError:
                continue
            album = parse.normalizeAlbum(song.metadata['album'])
            if album in albums and song.metadata['track'] in albums[album]:
                row = db_obj.insertMusicRow(
                    re.sub('\\s+', ' ', song.metadata['title']).strip(' '),
                    re.sub('\\s+', ' ', song.metadata['album']).strip(' '),
                    song.metadata['track'],
                    path
                )
                for mood in albums[album][song.metadata['track']]:
                    db_obj.insertAssociationRow(mood, row)
            song.stop()
    db_obj.commit()
