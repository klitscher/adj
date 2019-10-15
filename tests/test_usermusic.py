import adj.audio
import adj.db
import itertools
import os
import unittest


class TestUserMusic (unittest.TestCase):
    """test user music files are parsed correctly and inserted into db properly"""

    @classmethod
    def setUpClass(cls):
        """initialize Bass prior to all tests in order to view metadata"""
        adj.audio.init(0)
        db = adj.db.DataBase(':memory:')
        db.createTables()
        moods = [mood
        db.
        
        
    things_to_test = '''

    - user gives path to empty dir: test that db is empty
    - test that all relevant items are added to db
    - album match and track match: s
    - test associations worked
    - 
'''
    def testFullMatch(self):
        """album and track number matching result in every permutation"""
        master1 = {'first album': {1: {'ambivalent', 'sad', 'happy'}, 2: {'murder', 'morose'}}, 'second album': {300: {'this is all one mood', 'lemons', 'gingery'}}}
        master2 = {'first album': {2: {'murder', 'morose'}}, 'second album': {300: {'this is all one mood', 'lemons', 'gingery'}}}
        master3 = {'first album': {3: {'ambivalent', 'sad', 'happy'}, 2: {'murder', 'morose'}}, 'second album': {300: {'this is all one mood', 'lemons', 'gingery'}}}
        master4 = {'third album': {1: {'ambivalent', 'sad', 'happy'}, 2: {'murder', 'morose'}}, 'second album': {300: {'this is all one mood', 'lemons', 'gingery'}}}
        db._conn.execute('delete from music')
