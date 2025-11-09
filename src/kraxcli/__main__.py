import subprocess
import sys
import argparse
import json
from serial.tools import list_ports
from multiprocessing import Process
    
try:
    from .tools import tool_upydev,make_layout
except ImportError as e:
    from tools import tool_upydev,make_layout

def detect_type(args):
    try:
        if args.host is not None:
            return 'host'
        elif args.port is not None or args.serial:
            return 'serial'
        conf = json.load(open('upydev_.config','r+t'))
        if 'name' in conf and conf['name']=='usbdev':
            return 'serial'
    except Exception as e:
        print(f'Unexpected exception:{e}')
    return 'host'

def serials(args):
        sys.argv = ['pyserial-ports']+args+['-q','(USB|COM|ACM)']
        ports = list_ports.main()  # Вызываем функцию main из list_ports
        return ports

def vars(args):
    try:
        import re
        ret = subprocess.run(['python3','krax.py','--exports'],capture_output=True,text=True)
        print(ret.stdout)
        fake = []
        
        for line in str(ret.stdout).split('\n'):
            line = str(line).strip()
            match = re.search(r'^([^\.]*) AT',line)
            if match:
                fake.append(match.group(1))

        if len(fake)>0:
            print(f"""
#VSCode autocompleter блок.
from sys import platform
if platform=='vscode':
    from collections import namedtuple
    HW = namedtuple('HW',['{str('\',\'').join(fake)}'],defaults=[])
    hw = HW()
""")
                
    except Exception as e:
        print(f'Ошибка при запуске программы: {e}',file=sys.stderr)
    
def recheck(args):
    try:
        ret = subprocess.run(['python3','krax.py','--exports'],capture_output=True,text=True)
        return ret.returncode
    except Exception as e:
        print(f'Ошибка при запуске программы: {e}',file=sys.stderr)
    
def tool_mpremote(args,*_,**kwargs):
    sys.argv = ['mpremote']+args
    from mpremote import __main__

def fork_fun(fn,args):
    p = Process(target=fn,args=(args,))
    p.start()
    p.join()
    
def tool_telnet(*_,host:str,**kwargs):
    try:
        if host is None:
            conf = json.load(open('upydev_.config','r+t'))
            if 'addr' in conf:
                host = conf['addr']
        from sys import platform
        if platform!='linux':
            result = subprocess.run(['telnet',host],capture_output=False, text=True, check=True)
        else:
            tool_upydev(['repl'])
            return
            
    except Exception as e:
        print(f'🚫 Ошибка: {e}')
        return e
    return result.stdout

def tool_config(*_,port=None,host=None,password:str=None,**kwargs):
    try:
        if host is not None:
            tool_upydev(['config','-t',host,'-p',password,'-@','netdev'])
        elif port is not None:
            tool_upydev(['config','-t',port,'-p','115200','-@','usbdev'])
    except Exception as e:
        print(f'Unexpected exception:{e}')

routes = { 
            'stop' :{ 
                        'host': (tool_upydev, ['kbi'] ),
                        'serial': (tool_mpremote, ['soft-reset'])
                    },
            'repl' :{
                        'host': ( tool_telnet, [] ),
                        'serial': ( tool_mpremote, [] )
                    },
            'reset' :{ 
                        'host': (tool_upydev, ['reset'] ),
                        'serial': (tool_mpremote, ['reset'])
                    }
            }
excluded_files = '"*__pycache__*" "*/persist.*" "*/upydev_.*" "micropython.py" "webrepl_cfg.py"'
actions = {
            'serials': serials,
            'upydev' : tool_upydev,
            'mpremote': tool_mpremote,
            'run' : (tool_upydev,['run']),
            'compare' : (tool_upydev,['dsync','-fg','-n','-i',excluded_files]),
            'diff' : (tool_upydev,['dsync','-fg','-n','-p','-i',excluded_files]),
            'put' : (tool_upydev,['dsync','-fg','-i',excluded_files]),
            'get' : (tool_upydev,['dsync','-d','-fg','-i',excluded_files]),
            'check' : (tool_upydev,['cat','project.py']),
            'upload' : (tool_upydev,['-fg','put']),
            'download' : (tool_upydev,['-fg','get']),
            'load' : (tool_upydev,['load']),
            'config' : (tool_config,[]),
            'vars' : vars,
            'layout' : make_layout
        }

import os

def ensure_home_env():
    if 'HOME' not in os.environ:
        current_dir = os.getcwd()
        os.environ['HOME'] = current_dir

def main():
    parser = argparse.ArgumentParser(prog='kraxcli',description="Обертка для pyserial-ports/mpremote/upydev",add_help=True)
    parser.add_argument("--host",default=None, help='IP/хост устройства')
    parser.add_argument("--password",default='115200', help='Пароль')
    parser.add_argument("--port",default=None, help='COM-порт устройства')
    parser.add_argument("--dev",default='src', help='Расположение проекта')
    parser.add_argument("--recheck",action='store_true',help='Проверить проект')
    parser.add_argument("--serial",action='store_true',help='Предпочтительно по USB')
    subparsers = parser.add_subparsers(dest='action',required=True,help='Что нужно сделать')
    action_mpremote = subparsers.add_parser('mpremote')
    action_upydev = subparsers.add_parser('upydev')
    action_serials = subparsers.add_parser('serials', help='Список доступных портов')
    action_stop = subparsers.add_parser('stop', help='Остановить работу ПЛК')
    action_repl = subparsers.add_parser('repl', help='Запустить REPL')
    action_run = subparsers.add_parser('run', help='Запустить программу')
    action_reset = subparsers.add_parser('reset', help='Перезапустить контроллер')
    action_compare = subparsers.add_parser('compare', help='Сравнить проект с устройством')
    action_diff = subparsers.add_parser('diff', help='Сравнить проект с устройством и показать отличия')
    action_get = subparsers.add_parser('get', help='Скачать проект из устройством')
    action_put = subparsers.add_parser('put', help='Закачать проект в устройство')
    action_check = subparsers.add_parser('check', help='Проверить подключение к устройству')
    action_config= subparsers.add_parser('config', help='Настроить утилиту upydev')
    action_vars= subparsers.add_parser('vars', help='Получить переменные программы контроллера')
    action_layout= subparsers.add_parser('layout', help='Настроить модули ввода-вывода')
    action_download = subparsers.add_parser('download',help='Скачать файл из ПЛК')
    action_upload = subparsers.add_parser('upload',help='Закачать файл в ПЛК')
    action_load = subparsers.add_parser('load',help='Закачать файл в ПЛК и выполнить')
    action_download.add_argument('file',type=str,help='Имя файла')
    action_upload.add_argument('file',type=str,help='Имя файла')
    action_load.add_argument('file',type=str,help='Имя файла')
    for x in [action_mpremote,action_upydev,action_serials,action_stop,action_repl,action_run,action_reset,action_diff,action_get,action_put,action_compare,action_check,action_config,action_vars,action_upload,action_download,action_load,action_layout]:
        x.add_argument(
            'extra_args',
            nargs=argparse.REMAINDER,
            help="Дополнительные аргументы для передачи"
        )
    action_mpremote.set_defaults(tool=tool_mpremote)
    action_upydev.set_defaults(tool=tool_upydev)
    
    args,unknown = parser.parse_known_args()
    # настройка upydev
    ensure_home_env()
    
    try:
        os.chdir(args.dev)
    except FileNotFoundError:
        os.makedirs(args.dev,exist_ok=True)
        os.chdir(args.dev)
        print(f"Каталог проекта контроллера --dev={args.dev} не найден. Создаю...",file=sys.stderr)
        
    if args.recheck and recheck(args)!=0:
        print(f'В программе есть ошибки.')
        return

    if args.action in routes:
        device_type = detect_type(args)
        route = routes[args.action][device_type]
        route[0](route[1]+unknown+args.extra_args,port=args.port,host=args.host)
    elif args.action in actions:
        if args.action == 'check': detect_type(args)
        action = actions[args.action]
        if callable(action):
            actions[args.action]( unknown + args.extra_args )
        else:
            if args.action in ['upload','download','load']:
                action[0]( action[1] + unknown + args.extra_args+[args.file],port=args.port,host=args.host,password=args.password )
            else:
                action[0]( action[1] + unknown + args.extra_args,port=args.port,host=args.host,password=args.password )

if __name__ == "__main__":
    args = [arg for arg in sys.argv if not arg.startswith("parent_pid=")]
    if len(args)==len(sys.argv):
        os.system("")
        main()