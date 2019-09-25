#!/usr/bin/python3
"""Module to create a database"""


import sqlite3


def createDB(path=None):
    """Function to create a databases with required tables
    path: Optional argument to already created database
    """

    if path is None:
        connection = sqlite3.connect('./AmbientDJ_DB.sqlite3')
    else:
        connection = sqlite3.connect(path)
    cur = conection.cursor()
    music_sql = """CREATE TABLE IF NOT EXISTS music (
        id integer PRIMARY KEY,
        title text NOT NULL,
        trackNumber text NOTNULL,
        """
    
