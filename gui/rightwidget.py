"""Module for right side of GUI"""
import adj.playlist

import functools

import kivy.lang
import kivy.uix.boxlayout
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.properties import ListProperty

class RightWidget (kivy.uix.boxlayout.BoxLayout):
    """right side of gui class"""

    song_list = ListProperty()
            
    def activate_playlist(self):
        """call switchplaylist method of main widgit"""
        playlist = adj.playlist.Playlist(self.song_list)
        self.parent.switchPlaylist(playlist)
    
    def get_playlist(self, mood_dict):
        """query the db for list of songs matching filter"""
        if len(mood_dict) == 0:
            self.song_list = []
            self.ids.alt_plst.data = []
            return self.parent.db.getMoods()
        self.song_list = self.parent.db.filterMusic(mood_dict)
        self.ids.alt_plst.data = [{'text': song.title} for song in self.song_list]
        moods = functools.reduce(set.union, (song.moods for song in self.song_list), set())
        return moods

    def on_song_list(self, _self, value):
        """enable button"""
        if len(self.song_list) == 0:
            self.ids.activate.disabled = True
        else:
            self.ids.activate.disabled = False
