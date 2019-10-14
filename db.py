"""Module to create a database"""

import adj
import os
import parseMasterList
import sqlite3

class DataBase:
    """Class to instantiate db
    This will automatically connect to the db,
    but needs to be manually closed when all
    transaction are done by calling .close()
    """
    def __init__(self, path=os.path.join(adj.path, 'AmbientDJ_DB.sqlite3')):
        """Instantiates class
        path: path to the database
        """
        self._path = path
        self._conn = self.connect()
    
    def connect(self):
        """Method to connect to database"""
        connection = sqlite3.connect(self._path)

        """ Forcing foreign key constraints """
        connection.execute('PRAGMA foreign_keys = ON')
        return connection

    def close(self):
        """Method to close the db connection"""
        self._conn.commit()
        self._conn.close()

    def createTables(self):
        """Method to create tables in database"""

        music_sql = """CREATE TABLE IF NOT EXISTS music (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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

    def insertMusicRow(self, title, album, trackNumber,
                    pathToMusic,
                    pathToDb=os.path.join(adj.path, 'AmbientDJ_DB.sqlite3')):
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
        self._conn.execute(row_sql, (title, album, trackNumber, pathToMusic))
    
    def insertMoodRow(self, mood):
        """Method to insert a mood into db
        mood: mood to be added to db
        """
    
        mood_sql = """INSERT INTO moods(?)"""

        self._conn.execute(mood_sql, (mood))
