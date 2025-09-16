# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_all

upydev_dat,upydev_bin,upydev_imports = collect_all("upydev")
upydevice_dat,upydevice_bin,upydevice_imports = collect_all("upydevice")
mpremote_dat,mpremote_bin,mpremote_imports = collect_all("mpremote")
serial_dat,serial_bin,serial_imports = collect_all("serial")

a = Analysis(
    ['src/kraxcli/__main__.py'],
    pathex=[],
    binaries=serial_bin+mpremote_bin+upydev_bin+upydevice_bin+[('src/kraxcli/_upydev.py','.')],
    datas=serial_dat+mpremote_dat+upydev_dat+upydevice_dat,
    hiddenimports=serial_imports+mpremote_imports+upydev_imports+upydevice_imports+['packaging','packaging.version','argcomplete'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='kraxcli',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
