"""Module to create the GUI"""
import adj
import adj.db
import adj.masterlist
import adj.playlist
import adj.gui.leftwidget
import adj.gui.rightwidget
import kivy.app
from kivy.config import Config
import kivy.lang
import kivy.uix.boxlayout
import os.path

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
kivy.lang.Builder.load_file(os.path.join(adj.path, 'gui', 'adj.kv'))


class MainWidget (kivy.uix.boxlayout.BoxLayout):
    """Root of all the widgets"""
    db = None
    playlist = None

    def on_start(self):
        """Initialization function for widgets"""
        self.db = adj.db.DataBase(os.path.join(adj.path, 'adj.db'))
        self.playlist = adj.playlist.Playlist()

    def switchPlaylist(self, playlist):
        """switch the playlist from the current one to the one selected by the user"""
        if len(self.playlist) > 0:
            self.playlist.channel.stop()
        self.playlist = playlist
        self.playlist.onEnd = self.ids.left.songChanged
        self.ids.left.songChanged(self.playlist[0])
        self.playlist.channel.play()


class MainApp (kivy.app.App):
    """Kivy application"""

    def build(self):
        """Builds the gui"""
        self.root = MainWidget()
        return self.root
    
    def on_start(self, root=None):
        """Initialization of app"""
        if root is None:
            self.root.on_start()
            root = self.root
        for child in root.children:
            if hasattr(child, 'on_start'):
                child.on_start()
            self.on_start(child)
