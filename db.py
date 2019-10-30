"""Module to create a database"""

import adj
import collections
import itertools
import os
import sqlite3
import typing


Music = collections.namedtuple(
    'Music',
    ('id', 'title', 'album', 'number', 'path', 'moods')
)


class DataBase:
    """Class to instantiate db
    This will automatically connect to the db,
    but needs to be manually closed when all
    transaction are done by calling .close()
    """

    def __init__(self, path=os.path.join(adj.path, 'adj.db')):
        """Instantiates class
        path: path to the database
        """
        self._path = path
        self._conn = sqlite3.connect(path)
        self._conn.execute('PRAGMA foreign_keys = ON')

    def close(self, commit=True):
        """Method to close the db connection"""
        if commit:
            self._conn.commit()
        self._conn.close()

    def changeMoods(self, song: Music):
        """Change the moods associated with a song.
        
        The song parameter represents the desired song information. Its "id"
        attribute is used to look up the song record to update, and its "moods"
        attribute is used to remove moods not listed there and add ones that
        are.
        """
        queryDelete = "DELETE FROM music_moods WHERE track = ? and mood in ({})"
        queryInsert = "INSERT INTO music_moods (track, mood) VALUES {}"
        querySelect = "SELECT mood FROM music_moods WHERE track = ?"
        newMoods = song.moods
        cursor = self._conn.execute(querySelect, (song.id,))
        oldMoods = set(row[0] for row in cursor.fetchall())
        diff = oldMoods - newMoods
        if len(diff) > 0:
            queryDelete = queryDelete.format(
                ', '.join('?' for _ in range(len(diff)))
            )
            self._conn.execute(queryDelete, (song.id,) + tuple(diff))
        diff = newMoods - oldMoods
        if len(diff) > 0:
            queryInsert = queryInsert.format(
                ', '.join('(?, ?)' for _ in range(len(diff)))
            )
            params = tuple(
                item
                for pair in zip(itertools.repeat(song.id), diff)
                for item in pair
            )
            self._conn.execute(queryInsert, params)

    def createTables(self):
        """Method to create tables in database"""
        music_sql = """CREATE TABLE IF NOT EXISTS music (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            album TEXT NOT NULL,
            number INTEGER NOT NULL,
            path TEXT NOT NULL
            )
            """
        mood_sql = """CREATE TABLE IF NOT EXISTS moods (
            mood TEXT PRIMARY KEY
            )
            """
        association_sql = """CREATE TABLE IF NOT EXISTS music_moods (
            mood TEXT,
            track INTEGER,
            PRIMARY KEY (mood, track)
            FOREIGN KEY(mood) REFERENCES moods ON DELETE CASCADE,
            FOREIGN KEY(track) REFERENCES music ON DELETE CASCADE
            )
            """
        self._conn.execute(music_sql)
        self._conn.execute(mood_sql)
        self._conn.execute(association_sql)

    def filterMusic(self, filter: typing.Dict[str, bool]) -> typing.List[Music]:
        """Get music from the database matching the given mood filter.

        The filter dictionary's keys are the mood names. If the value is
        False, then only songs without that mood are returned; and if the value
        is True, only songs with that mood are returned.
        """
        query = '''
            SELECT id, title, album, number, path, group_concat(mood, "\x1F")
            FROM music JOIN music_moods ON track = id GROUP BY id
        '''
        if len(filter) > 0:
            template = 'sum(CASE WHEN mood = ? THEN 1 ELSE 0 END) {} 0'
            having = ' HAVING ' + ' and '.join(
                template.format('>' if include else '=')
                for include in filter.values()
            )
        cursor = self._conn.execute(
            query + having,
            tuple(mood for mood in filter.keys())
        )
        return [
            Music(id, title, album, number, path, set(moods.split('\x1F')))
            for id, title, album, number, path, moods in cursor.fetchall()
        ]

    def getMoods(self) -> typing.Set[str]:
        """Get the list of all moods."""
        cursor = self._conn.execute('SELECT mood FROM moods')
        return set(row[0] for row in cursor.fetchall())

    def getMusic(self, title=None, album=None, path=None) -> typing.List[Music]:
        """Get all songs or the song(s) matching given keyword arguments."""
        filters = (('title', title), ('album', album), ('path', path))
        if title is not None or album is not None or path is not None:
            where = ' WHERE ' + ' and '.join(
                name + ' = ?'
                for name, value in filters
                if value is not None
            )
        else:
            where = ''
        cursor = self._conn.execute(
            'SELECT id, title, album, number, path FROM music' + where,
            tuple(value for name, value in filters if value is not None)
        )
        return [Music(*row + (set(),)) for row in cursor.fetchall()]

    def insertAssociation(self, mood, track):
        """Method to insert a row into the association table.
        mood: name of mood
        track: row ID of track from music table
        """
        row_sql = 'INSERT INTO music_moods(mood, track) VALUES (?, ?)'
        cursor = self._conn.execute(row_sql, (mood, track))
        return cursor.lastrowid

    def insertMusic(self, title, album, trackNumber, pathToMusic):
        """Method to insert a row into the music table
        title: title of the song
        album: album song is on
        trackNumber: track number of the song
        pathToMusic: path to the song in the user's music library
        pathToDb: path to the sqlite database
        """
        row_sql = """INSERT INTO music(title, album, number, path)
            VALUES(?, ?, ?, ?)
            """
        cursor = self._conn.execute(
            row_sql,
            (title, album, trackNumber, pathToMusic)
        )
        return cursor.lastrowid

    def insertMood(self, mood):
        """Method to insert a mood into db
        mood: mood to be added to db
        """
        mood_sql = """INSERT INTO moods VALUES(?)"""

        cursor = self._conn.execute(mood_sql, (mood,))
        return cursor.lastrowid

    def populated(self):
        query = '''
            SELECT count(*) FROM sqlite_master
            WHERE type = "table" and name in (?, ?, ?)
        '''
        cursor = self._conn.execute(query, ('music', 'moods', 'music_moods'))
        return cursor.fetchone()[0] >= 3
