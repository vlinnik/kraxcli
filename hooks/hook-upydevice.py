from PyInstaller.utils.hooks import collect_all,collect_submodules
import shutil
# datas,binaries,hiddenimports = collect_all("upydev")

datas,binaries,hiddenimports = collect_all("upydevice")
datas += [ ('.venv/lib/python3.12/site-packages/upydev','upydev') ] 

upydev_path = shutil.which("upydev")
binaries+=[(upydev_path,'bin')]
hiddenimports+=collect_submodules('upydev')

web_repl_path = shutil.which("web_repl")
binaries+=[(web_repl_path,'bin')]
