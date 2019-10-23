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
        music1 = self.data.getMusic(title='its')
        music2 = self.data.getMusic(album='a fun')
        music3 = self.data.getMusic(path='/song')
        music4 = self.data.getMusic(album='a fun', title='its')
        musicControl1 = [Music(title='its', album='a fun', number=1, path='/song', moods=set())]
        self.assertEqual(musicControl1, music1)
        self.assertEqual(musicControl1, music2)
        self.assertEqual(musicControl1, music3)
        self.assertEqual(musicControl1, music4)

        self.data.insertMusic('more', 'a fun', 2, '/song1')
        musicControl2 = [Music(title='more', album='a fun', number=2, path='/song1', moods=set())]
        music5 = self.data.getMusic(title='more')
        self.assertEqual(musicControl2, music5)
        
        musicControl3 = [Music(title='its', album='a fun', number=1, path='/song', moods=set()), 
                         Music(title='more', album='a fun', number=2, path='/song1', moods=set())]
        music6 = self.data.getMusic(album='a fun')
        self.assertEqual(musicControl3, music6)

    def testGetMoods(self):
        """Tests retrieving moods from the db"""
        self.data.createTables()
        self.data.insertMood('happy')
        self.data.insertMood('sad')
        self.data.insertMood('silly')
        moods = self.data.getMoods()
        moods1 = {'happy', 'sad', 'silly'}
        self.assertEqual(moods, moods1)
        
    def testFilterMusic(self):
        """Tests filterMusic function"""
        from db import Music
        self.data.createTables()
        self.data.insertMood('happy')
        self.data.insertMood('sad')
        self.data.insertMood('silly')
        self.data.insertMusic('its', 'a fun', 1, '/song')
        self.data.insertMusic('more', 'a fun', 2, '/song1')
        self.data.insertMusic('test', 'a fun', 3, '/song2')
        self.data.insertAssociation('happy', 1)
        self.data.insertAssociation('sad', 2)
        self.data.insertAssociation('silly', 1)
        self.data.insertAssociation('silly', 3)
        music1 = self.data.filterMusic({'happy': True})
        music2 = self.data.filterMusic({'silly': True})
        music3 = self.data.filterMusic({'silly': False, 'happy': False})
        control1 = [Music(title='its', album='a fun', number=1, path='/song', moods={'silly', 'happy'})] 
        control2 = [Music(title='its', album='a fun', number=1, path='/song', moods={'silly', 'happy'}),
                    Music(title='test', album='a fun', number=3, path='/song2', moods={'silly'})]
        control3 = [Music(title='more', album='a fun', number=2, path='/song1', moods={'sad'})]
        self.assertEqual(control1, music1)
        self.assertEqual(control2, music2)
        self.assertEqual(control3, music3)
