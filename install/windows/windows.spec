# -*- mode: python ; coding: utf-8 -*-

import os
from kivy_deps import sdl2, glew

block_cipher = None


a = Analysis(['adj\\__main__.py'],
             pathex=['.'],
             binaries=[('adj\\install\\windows\\bass.dll', '.'), ('adj\\install\\windows\\tags.dll', '.')],
             datas=[('adj\\gui\\adj.kv', 'adj\\gui'), ('adj\\gui\\left.kv', 'adj\\gui'), ('adj\\gui\\right.kv', 'adj\\gui'), ('adj\\gui\\config.kv', 'adj\\gui'), ('adj\\allmoods.txt', 'adj')],
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
coll = COLLECT(exe, Tree('adj'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='__main__')

os.rename('.\dist\__main__\__main__', r'.\dist\__main__\adj.exe')
os.rename(r'.\dist\__main__', r'.\dist\adj_package')