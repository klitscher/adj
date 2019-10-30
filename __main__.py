import adj
import adj.audio
import adj.gui.app
import adj.gui.firstrun
import ctypes
import multiprocessing
import os.path


multiprocessing.set_start_method('spawn')
multiprocessing.freeze_support()
if adj.platform.os == 'windows':
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

adj.audio.init()
adj.gui.app.MainApp().run()
