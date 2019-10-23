# -*- mode: python ; coding: utf-8 -*-

import os

os.system('cp adj/install/linux/libtags.so adj/install/linux/libbass.so adj/')

block_cipher = None


a = Analysis(['adj/__main__.py'],
             pathex=['/home/kyle/test'],
             binaries=[('./adj/libbass.so', '.'), ('./adj/libtags.so','.')],
             datas=[('./adj/gui/config.kv', 'adj/gui/'),
                    ('./adj/gui/adj.kv', 'adj/gui/'),
                    ('./adj/gui/left.kv', 'adj/gui/'),
                    ('./adj/gui/right.kv', 'adj/gui/'),
                    ('./adj/allmoods.txt', 'adj/')],
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


