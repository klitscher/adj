import kivy.properties
import kivy.uix.boxlayout


class SongInfo (kivy.uix.boxlayout.BoxLayout):
    title = kivy.properties.StringProperty('title')
    album = kivy.properties.StringProperty('album')
    track = kivy.properties.StringProperty('0')


class SongViewer(kivy.uix.boxlayout.BoxLayout):
    """widget to view and modify active playlist"""
    def on_activate(self):
        """display """
        self.ids.current_plst.data = [
            {'title': song.title, 'album': song.album, 'track': str(song.number)}
            for song in self.playlist
        ]
