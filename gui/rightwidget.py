"""Module for right side of GUI"""
import adj.playlist

import kivy.lang
import kivy.uix.boxlayout
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView


class RightWidget (kivy.uix.boxlayout.BoxLayout):
    """right side of gui class"""

    
    alt_playlist = None

    
    def on_start(self):
        """dynamically create playlist view and render activate button"""
        self.alt_playlist = self.parent.playlist
        self.ids.alt_plst.data = [{'text': song.title} for song in self.alt_playlist]

""" class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': str(x) for x in range(100)}]
 """
