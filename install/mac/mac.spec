# -*- mode: python ; coding: utf-8 -*-

import os
import shutil

os.system('cp adj/install/mac/libtags.dylib adj/install/mac/libbass.dylib adj/')

block_cipher = None

base = os.getcwd() + '/'
a = Analysis([base + 'adj/__main__.py'],
             pathex=[os.getcwd()],
             binaries=[(base + 'adj/libbass.dylib', '.'), (base + 'adj/libtags.dylib','.')],
             datas=[(base + 'adj/gui/config.kv', 'adj/gui/'),
                    (base + 'adj/gui/adj.kv', 'adj/gui/'),
                    (base + 'adj/gui/left.kv', 'adj/gui/'),
                    (base + 'adj/gui/right.kv', 'adj/gui/'),
                    (base + 'adj/allmoods.txt', 'adj/')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='__main__',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='__main__')

os.rename('./dist/__main__/__main__', './dist/__main__/adj.exe')
os.rename('./dist/__main__', './dist/adj_package')

os.mkdir('dist/adj_package/tk')
os.mkdir('dist/adj_package/tcl')
shutil.copyfile('/System/Library/Frameworks/Tcl.framework/Tcl', 'dist/adj_package/tcl/Tcl')
shutil.copyfile('/System/Library/Frameworks/Tk.framework/Tk', 'dist/adj_package/tk/Tk')
