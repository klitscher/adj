"""Module to create the GUI"""
import adj
import adj.db
import adj.masterlist
import adj.playlist
import adj.gui.leftwidget
import adj.gui.rightwidget
import adj.gui.songview
import kivy.app
import kivy.config
import kivy.lang
import kivy.properties
import kivy.uix.boxlayout
import os.path

kivy.config.Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
kivy.lang.Builder.load_file(os.path.join(adj.path, 'gui', 'adj.kv'))


class MainWidget (kivy.uix.boxlayout.BoxLayout):
    """Root of all the widgets"""
    db = kivy.properties.ObjectProperty(None, baseclass=adj.db.DataBase)
    playlist = kivy.properties.ObjectProperty(
        adj.playlist.Playlist(),
        baseclass=adj.playlist.Playlist
    )

    def on_start(self):
        """Initialization function for widgets"""
        self.db = adj.db.DataBase(os.path.join(adj.path, 'adj.db'))
        self._playlist = self.playlist
        self.remove_widget(self.playlistView)

    def on_playlist(self, _, playlist):
        """switch the playlist from the current one to the one selected by the user"""
        if len(self._playlist) > 0:
            self._playlist.channel.stop()
        self._playlist = playlist
        playlist.onEnd = self.ids.left.songChanged
        self.ids.left.songChanged(playlist[0])
        playlist.channel.play()

    def switch_view(self, which):
        if which == 'filter':
            self.remove_widget(self.playlistView)
            self.add_widget(self.filterView)
        elif which == 'playlist':
            self.remove_widget(self.filterView)
            self.add_widget(self.playlistView)


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
