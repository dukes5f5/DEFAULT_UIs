# main.spec
# PyInstaller spec file for myApp

from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
import os

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=collect_data_files('resources', includes=['*']) + [('license.dat', '.')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='myApp',  # Executable name: myApp.exe
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # ✅ Hide console window
    icon='resources/images/logo.ico'  # ✅ Set application icon
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='myApp'  # Output folder: dist/myApp/
)