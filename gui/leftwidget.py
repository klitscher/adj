"""Module for left side of GUI"""
import adj
import kivy.uix.boxlayout
from kivy.metrics import dp
from kivy.uix.button import Button


class LeftWidget (kivy.uix.boxlayout.BoxLayout):
    """Left side of gui class"""

    mood_dict = {}
    
    def on_start(self):
        """Set up for GUI"""
        self.mood_list = sorted(self.parent.db.getMoods())
        for mood in self.mood_list:
            button = Button(text=mood,
                            width=dp(100),
                            size_hint=(None, .1))
            button.bind(on_press=self.filter)
            self.ids.mood_grid.add_widget(button)
        
    def songChanged(self, song):
        """Change the displayed and playing song"""
        self.ids.title.text = song.title
        self.ids.album.text = song.album

    def playPause(self):
        """Plays or pauses a song based on its state"""
        if self.parent.playlist.channel.playing == True:
            self.parent.playlist.channel.pause()
            self.ids.play.text = 'Play'
        else:
            self.parent.playlist.channel.play()
            self.ids.play.text = 'Pause'

    def nextSong(self):
        """Skip to the next song in the playlist"""
        self.parent.playlist.next()

    def filter(self, button):
        """Callback function for clicking on moods"""
        if button.last_touch.button == 'left':
            self.mood_dict[button.text] = True
        else:
            self.mood_dict.pop(button.text, None)
        
