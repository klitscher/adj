import adj
import adj.db
import adj.masterlist
import adj.playlist
import adj.gui.leftwidget
import adj.gui.rightwidget
import kivy.app
import kivy.lang
import kivy.uix.boxlayout
import os.path


kivy.lang.Builder.load_file(os.path.join(adj.path, 'gui', 'adj.kv'))


class MainWidget (kivy.uix.boxlayout.BoxLayout):
    db = None
    playlist = None

    def on_start(self):
        self.db = adj.db.DataBase(os.path.join(adj.path, 'adj.db'))
        self.db.createTables()
        adj.masterlist.parseMasterList(
            os.path.join(adj.path, 'allmoods.txt'),
            self.db
        )
        self.playlist = adj.playlist.Playlist()


class MainApp (kivy.app.App):
    def build(self):
        self.root = MainWidget()
        return self.root
    def on_start(self, root=None):
        if root is None:
            self.root.on_start()
            root = self.root
        for child in root.children:
            if hasattr(child, 'on_start'):
                child.on_start()
            self.on_start(child)
