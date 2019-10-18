from kivy.app import App
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel

class adjTabs(TabbedPanel):
    mood_list = ['action', 'adventure', 'boss', 'bustle', 'carnival',
                 'cave', 'city', 'climax', 'danger', 'discovery',
                 'dread', 'eeriness', 'failure', 'falling', 'finality',
                 'happiness', 'haste', 'hope', 'industry', 'military',
                 'mystery', 'nobility', 'party', 'quiet', 'quirk',   
                 'relief', 'reverence', 'rising', 'sadness', 'safety',
                 'stealth', 'tension', 'town', 'victory', 'wilderness']
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for mood in self.mood_list:
            button = Button(text=mood, width=dp(100), size_hint=(None, .1))
            self.ids.mood_grid.add_widget(button)

class adjApp(App):
    def build(self):
        return adjTabs()
if __name__ == '__main__':
    adjApp().run()