"""Module for right side of GUI"""
import adj.playlist

import functools

import kivy.lang
import kivy.uix.boxlayout
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.properties import ListProperty, ObjectProperty

class RightWidget (kivy.uix.boxlayout.BoxLayout):
    """right side of gui class"""

    song_list = ListProperty()
            
    def activate_playlist(self):
        """call switchplaylist method of main widgit"""
        playlist = adj.playlist.Playlist(self.song_list)
        self.currentPlaylist = playlist
    
    def get_playlist(self, mood_dict):
        """query the db for list of songs matching filter"""
        if len(mood_dict) == 0:
            self.song_list = []
            self.ids.alt_plst.data = []
            self.ids.num_songs.text = ''
            return self.db.getMoods()
        self.song_list = self.db.filterMusic(mood_dict)
        self.ids.num_songs.text = '[size=50][b]' + str(len(self.song_list)) + '[/b][/size]'
        self.ids.alt_plst.data = [{'text': song.title} for song in self.song_list]
        moods = functools.reduce(set.union, (song.moods for song in self.song_list), set())
        return moods

    def on_song_list(self, _self, value):
        """enable/disable button"""
        if len(self.song_list) == 0:
            self.ids.activate.disabled = True
        else:
            self.ids.activate.disabled = False
