import subprocess
import typer
import json
import sys
import os
from typing import Optional

def detect_type():
    try:
        conf = json.load(open('upydev_.config','r+t'))
        if conf.get('name')=='usbdev':
            return 'serial'
        return 'host'                
    except FileNotFoundError:
        pass
    except Exception as e:
        typer.secho(f'Случилось страшное, {e}',bold=True,err=True)
    return 'serial'

def mpremote(*args:str):
    import sys
    saved = sys.argv 
    sys.argv = ['mpremote'] + list(args)
    try:
        from mpremote import __main__
    except SystemExit:
        pass
    except Exception as e:
        typer.secho(f'Случилось непоправимое, {e}',bold=True,err=True)
    sys.argv = saved
    
def upydev(*args: str):
    upydev_path: Optional[str]
    if getattr(sys, 'frozen', False):
        upydev_path = os.path.join(sys._MEIPASS,'bin','upydev')
        os.environ['PATH'] = os.environ['PATH']+os.pathsep+os.path.join(sys._MEIPASS,'bin')
    else:
        import shutil
        import site
        import sysconfig
        os.environ['PATH'] = os.environ.get('PATH','.')+os.pathsep+os.pathsep.join([os.path.join(p,'bin') for p in site.getsitepackages()])+os.pathsep+sysconfig.get_paths()['scripts']
        
        upydev_path = shutil.which("upydev")

    if not upydev_path:
        return
    saved = sys.argv
    # Чтение и выполнение кода
    with open(upydev_path, 'r', encoding='utf-8') as f:
        code = f.read()
        sys.argv = ['upydev']+list(args)
        env = {'__file__': upydev_path, '__name__': '__main__'}
        try:
            exec(code,env)  # Эмулируем __main__
        except SystemExit:
            pass
        except Exception as e:
            typer.secho(f'Случилось страшное, {e}',bold=True,err=True)
            # import traceback; traceback.print_exc();
        finally:    #почистим следы от использования upydev
            unload = [ x for x in sys.modules if 'upydev' in x ]
            for m in unload:
                sys.modules.pop(m)                    
            
    sys.argv = saved
    return

def telnet(host:Optional[str]=None):
    try:
        if host is None:
            conf = json.load(open('upydev_.config','r+t'))
            if 'addr' in conf:
                host = conf['addr']
        if host:
            result = subprocess.run(['telnet',host],capture_output=False, text=True, check=True)
    except Exception as e:
        typer.secho(f'Случилось страшное, {e}',bold=True,err = True)
        return e
    return result.stdout
