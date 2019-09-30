#!/usr/bin/python3
"""Module to create a database"""


import sqlite3


def createDB(path=None):
    """Function to create a databases with required tables
    path: Optional argument to already created database
    """

    """ Forcing foreign key constraints """

    if path is None:
        connection = sqlite3.connect('./AmbientDJ_DB.sqlite3')
    else:
        connection = sqlite3.connect(path)

    connection.execute('PRAGMA foreign_keys = ON')

    music_sql = """CREATE TABLE IF NOT EXISTS music (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        album TEXT NOT NULL,
        trackNumber TEXT NOT NULL,
        pathToFile TEXT NOT NULL
        )
        """
    atmosphere_sql = """CREATE TABLE IF NOT EXISTS atmospheres (
        scenes TEXT PRIMARY KEY
        )
        """
    association_sql = """CREATE TABLE IF NOT EXISTS atmosphereIndex (
        scenes TEXT,
        music_id INTEGER,
        PRIMARY KEY (scenes, music_id)
        FOREIGN KEY(scenes) REFERENCES atmosphere_sql(scenes) ON DELETE CASCADE,
        FOREIGN KEY(music_id) REFERENCES
            music_sql(id) ON DELETE CASCADE
        )
        """
    connection.execute(music_sql)
    connection.execute(atmosphere_sql)
    connection.execute(association_sql)

    connection.commit()
    connection.close()
