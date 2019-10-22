import adj
import adj.audio
import adj.gui.app
import adj.gui.firstrun
import multiprocessing
import os.path

if adj.platform.os == 'mac':
    multiprocessing.set_start_method('spawn')

adj.audio.init()
if not os.path.isfile(os.path.join(adj.path, 'adj.db')):
    proc = multiprocessing.Process(target=adj.gui.firstrun.subProcMain)
    proc.start()
    proc.join()
adj.gui.app.MainApp().run()
