import adj
import adj.audio
import adj.db
import adj.gui.app
import adj.gui.firstrun
import ctypes
import multiprocessing
import os.path


if adj.platform.os == 'mac':
    multiprocessing.set_start_method('spawn')
    multiprocessing.freeze_support()
if adj.platform.os == 'windows':
    multiprocessing.set_start_method('spawn')
    multiprocessing.freeze_support()
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

adj.audio.init()
if not adj.db.DataBase().populated():
    proc = multiprocessing.Process(target=adj.gui.firstrun.subProcMain)
    proc.start()
    proc.join()
adj.gui.app.MainApp().run()
