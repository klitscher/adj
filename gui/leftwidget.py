import kivy.uix.boxlayout
from kivy.metrics import dp
from kivy.uix.button import Button


class LeftWidget (kivy.uix.boxlayout.BoxLayout):
    def on_start(self):
        self.mood_list = sorted(self.parent.db.getMoods())
        for mood in self.mood_list:
            button = Button(text=mood, width=dp(100), size_hint=(None, .1))
            self.ids.mood_grid.add_widget(button)

    def songChanged(self, song):
        self.ids.title.text = song.title
        self.ids.album.text = song.album
