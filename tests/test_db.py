#!/usr/bin/python3
"""Test module for the database code"""

import adj
from adj import db
import os
import sqlite3
import typing
import unittest



class TestDbMethods(unittest.TestCase):
    """Class for all the db method tests"""

    def setUp(self):
        self.data = db.DataBase(path=':memory:')

    def tearDown(self):
        """Deletes the db when method is run"""
        self.data._conn.close()

    def testCreateTables(self):                                                 
        """Tests that tables are created in the db"""                           
        self.data.createTables()
        self.data._conn.commit()
        res = self.data._conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [val for val in res]
        self.assertEqual(tables, [('music',), ('moods',), ('music_moods',)])

    def testClose(self):
        """Tests the clsoe method"""
        self.data.createTables()
        self.data.close()
        self.assertRaises(sqlite3.ProgrammingError, 
                          self.data._conn.execute, 
                          "SELECT name FROM sqlite_master WHERE type='table'")

    def testInsertMusic(self):
        """Tests inserting music into db"""
        self.data.createTables()
        self.data.insertMusic('test', 'test', 100, '/test')
        self.data._conn.commit()
        res = self.data._conn.execute("Select * from music").fetchall()
        self.assertEqual(res, [(1, 'test', 'test', 100, '/test')])

    def testInsertMood(self):
        """Tests inserting music into db"""
        self.data.createTables()
        self.data.insertMood('test')
        self.data._conn.commit()
        res = self.data._conn.execute("Select * from moods").fetchall()
        self.assertEqual(res, [('test',)])


    def testInsertAssociation(self):
        """Tests inserting music into db"""
        self.data.createTables()
        self.data.insertMood('mood')
        self.data.insertMusic('test', 'test', 100, '/test')
        self.data.insertAssociation('mood', 1)
        self.data._conn.commit()
        res = self.data._conn.execute("Select * from music_moods").fetchall()
        self.assertEqual(res, [('mood', 1)])

    def testGetMusic(self):
        """Tests retrieving music from the db"""
        Music = adj.db.Music
        self.data.createTables()
        self.data.insertMood('happy')
        self.data.insertMusic('its', 'a fun', 1, '/song')
        self.data.insertAssociation('happy', 1)
        music = self.data.getMusic(title='its')
        music2 = [Music(title='its', album='a fun', number=1, path='/song', moods=set())]
        self.assertEqual(music, music2)
