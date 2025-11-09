from PyInstaller.utils.hooks import collect_all,collect_submodules
import shutil

upydev_path = shutil.which("upydev")

_,binaries,hiddenimports = collect_all("upydev")
binaries+=[(upydev_path,'bin')]
datas = [ ('.venv/lib/python3.12/site-packages/upydev','__upydev') ] 
