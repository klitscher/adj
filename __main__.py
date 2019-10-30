import adj
import adj.audio
import adj.gui.app
import adj.gui.firstrun
import ctypes
import multiprocessing
import os.path


if adj.platform.os == 'mac':
    multiprocessing.set_start_method('spawn')
    multiprocessing.freeze_support()
elif adj.platform.os == 'windows':
    multiprocessing.freeze_support()
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

adj.audio.init()
adj.gui.app.MainApp().run()
