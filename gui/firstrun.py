import adj
import adj.audio
import adj.db
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
    """Entry point for the configuration screen's subprocess."""
    ConfigApp().run()


if adj.platform.os == 'windows':
    class WindowsDrives (kivy.uix.stacklayout.StackLayout):
        """A stack of buttons listing the drives available on Windows.
        
        This is necessary because Kivy's file browser isn't aware of drives.
        """
        def __init__(self, **kwargs):
            """Create a row of buttons to allow selecting Windows drives."""
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
            """Tell the file browser to switch Windows drives.
            
            This is used as the callback for the drive buttons ("C:", "E:").
            It also clears the current selected file.
            """
            self.parent.ids.browser.path = button.text
            self.parent.ids.browser.selection = []


class ConfigWidget (kivy.uix.boxlayout.BoxLayout):
    """Root widget for the configuration screen."""

    def on_start(self):
        """If running on Windows, creates buttons to switch drives."""
        if adj.platform.os == 'windows':
            self.add_widget(WindowsDrives(), 2)

    def changeSelection(self):
        """Update the text box with the current selection."""

    def chooseLibrary(self):
        """Loads music from the provided directory, populating the database.
        
        This is used as the "Choose Library" button callback.
        """
        if len(self.ids.browser.selection) > 0:
            libraryPath = self.ids.browser.selection[0]
            listPath = os.path.join(adj.path, 'allmoods.txt')
            db = adj.db.DataBase(os.path.join(adj.path, 'adj.db'))
            db.createTables()
            albumMoods = adj.masterlist.parseMasterList(listPath, db)
            adj.usermusic.populateMusic(libraryPath, db, albumMoods)
            db.close()
            kivy.app.App.get_running_app().stop()

    def onlyDirectories(self, dirName, fileName):
        """Reject all files so only directories are selectable."""
        return False


class ConfigApp (kivy.app.App):
    def build(self):
        """Create the root widget."""
        adj.audio.init(0)
        self.root = ConfigWidget()
        return self.root

    def on_start(self):
        """Signal the root widget that it can safely initialize."""
        self.root.on_start()
