"""Module to create a database"""

import adj
import collections
import os
import sqlite3
import typing


Music = collections.namedtuple('Music', ('title', 'album', 'number', 'path'))



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

    def getMoods(self) -> typing.List[str]:
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
            'SELECT title, album, number, path FROM music' + where,
            tuple(value for name, value in filters if value is not None)
        )
        return [Music(*row) for row in cursor.fetchall()]

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
