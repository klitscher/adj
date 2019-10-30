"""Module for left side of GUI"""
import adj
import kivy.uix.boxlayout
from kivy.clock import mainthread
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.properties import StringProperty

class LeftWidget (kivy.uix.boxlayout.BoxLayout):
    """Left side of gui class"""

    mood_dict = {}
    
    def on_start(self):
        """Set up for GUI"""
        self.mood_list = sorted(self.db.getMoods())
        for mood in self.mood_list:
            button = FilterButton(text=mood,
                            width=dp(100),
                            size_hint=(None, .1))
            button.bind(on_press=self.filter)
            self.ids.mood_grid.add_widget(button)

    @mainthread
    def songChanged(self, song):
        """Change the displayed and playing song"""
        if song is None:
            self.ids.play.text = 'Stopped'
            return
        self.ids.title.text = song.title
        self.ids.album.text = song.album
        self.ids.play.text = 'Pause'

    def playPause(self):
        """Plays or pauses a song based on its state"""
        if self.playlist.channel is None:
            return
        if self.playlist.channel.stopped:
            return            
        if self.playlist.channel.playing == True:
            self.playlist.channel.pause()
            self.ids.play.text = 'Play'
        else:
            self.playlist.channel.play()
            self.ids.play.text = 'Pause'

    def nextSong(self):
        """Skip to the next song in the playlist"""
        if self.playlist.channel is None:
            return
        self.playlist.next()

    def filter(self, button):
        """Callback function for clicking on moods"""
        if button.filterState == 'unavailable':
            pass
        else:
            if (button.filterState == 'included' and
                button.last_touch.button == 'left'
            ):
                self.mood_dict.pop(button.text, None)
                button.filterState = 'available'
            elif (button.filterState == 'excluded' and
                  button.last_touch.button == 'right'
            ):
                self.mood_dict.pop(button.text, None)
                button.filterState = 'available'
            elif button.last_touch.button == 'left':
                self.mood_dict[button.text] = True
                button.filterState = 'included'
            elif button.last_touch.button == 'right':
                self.mood_dict[button.text] = False
                button.filterState = 'excluded'
            available_moods = self.sibling.get_playlist(self.mood_dict)
            for childButton in self.ids.mood_grid.children:
                if childButton.filterState in ('included', 'excluded'):
                    continue
                if childButton.text in available_moods:
                    childButton.filterState = 'available'
                else:
                    childButton.filterState = 'unavailable'
                    
class FilterButton(ButtonBehavior, Widget):
    """Class for custom buttons"""

    filterState = StringProperty('available')
    text = StringProperty('default')
    
    def __init__(self, **kwargs):
        """Initializtion of button instance"""
        self.text = kwargs.pop('text', 'default')
        super().__init__(**kwargs)

    def on_filterState(self, _, state):
        """Changes button color based on state"""
        if state == 'unavailable':
            self.borderColor = [.2, .2, .2]
            self.fillColor = [.2, .2, .2]
            return
        self.fillColor = [.4, .4, .4]
        if state == 'available':
            self.borderColor = [.4, .4, .4]
        if state == 'included':
            self.borderColor = [.3, 1, .3]
        if state == 'excluded':
            self.borderColor = [1, .3, .3]
