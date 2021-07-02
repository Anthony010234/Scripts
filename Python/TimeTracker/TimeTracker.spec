# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['TimeTracker.py'],
             pathex=['C:\\Users\\Owner\\Documents\\GitHub\\TSF-INTERNAL\\Python Scripts\\TimeTracker'],
             binaries=[],
             datas=[],
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
          name='TimeTracker',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='stopwatch_icon-icons.com_64805.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='TimeTracker')
