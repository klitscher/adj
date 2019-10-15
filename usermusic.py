import adj
import adj.audio
import adj.db
import adj.parseMasterList as parse
import os
import re


def load_music(music_root, db_obj):
    """parse user music and store matching items in db"""

    albums = parse.parseMasterList(os.path.join(adj.path, 'allmoods.txt'))

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
    db_obj.commit()
