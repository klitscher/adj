import adj
import adj.audio
import adj.db
import adj.gui.filebrowser
import adj.masterlist
import adj.usermusic
import ctypes
import kivy.app
import kivy.lang
import kivy.metrics
import kivy.uix.boxlayout
import kivy.uix.button
import kivy.uix.stacklayout
import os.path
import string


def subProcMain():
    ConfigApp().run()


if adj.platform.os == 'windows':
    class WindowsDrives (kivy.uix.stacklayout.StackLayout):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.orientation = 'lr-tb'
            self.size_hint_y = .1
            bits = ctypes.windll.kernel32.GetLogicalDrives()
            drives = [
                letter
                for index, letter in enumerate(string.ascii_uppercase)
                if bits & (1 << index) > 0
            ]
            for drive in drives:
                button = kivy.uix.button.Button(text=drive + ':')
                button.bind(on_press=self.changeDrive)
                button.size_hint_x = None
                button.width = kivy.metrics.dp(80)
                self.add_widget(button)

        def changeDrive(self, button):
            self.parent.ids.browser.path = button.text
            self.parent.ids.browser.selection = []


class ConfigWidget (kivy.uix.boxlayout.BoxLayout):
    def on_start(self):
        if adj.platform.os == 'windows':
            self.add_widget(WindowsDrives(), 2)

    def chooseLibrary(self):
        if len(self.ids.browser.selection) > 0:
            libraryPath = self.ids.browser.selection[0]
            listPath = os.path.join(adj.path, 'allmoods.txt')
            db = adj.db.DataBase(os.path.join(adj.path, 'adj.db'))
            db.createTables()
            albumMoods = adj.masterlist.parseMasterList(listPath, db)
            adj.usermusic.populateMusic(libraryPath, db, albumMoods)
            db.close()
            kivy.app.App.get_running_app().stop()

    def toggleButton(self):
        self.ids.select.disabled = len(self.ids.browser.selection) < 1

    def onlyDirectories(self, dirName, fileName):
        return False


class ConfigApp (kivy.app.App):
    def build(self):
        adj.audio.init(0)
        self.root = ConfigWidget()
        return self.root

    def on_start(self):
        self.root.on_start()
