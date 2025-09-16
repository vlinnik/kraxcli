import subprocess
import sys
import argparse
from serial.tools import list_ports
from multiprocessing import Process

def detect_type(args):
    if args.host is not None:
        fork_fun(tool_upydev,['config','-t',args.host,'-p',args.password])
        return 'host'
    elif args.port is not None:
        fork_fun(tool_upydev,['config','-t',args.port,'-p',args.password])
    return 'serial'

def serials(args):
        sys.argv = ['pyserial-ports']+args+['-q','(USB|COM|ACM)']
        ports = list_ports.main()  # Вызываем функцию main из list_ports
        return ports

def tool_mpremote(args,*_,**kwargs):
    sys.argv = ['mpremote']+args
    from mpremote import __main__

def tool_upydev(args,*_,**kwargs):
    sys.argv = ['upydev']+args
    # print(sys.argv)
    try:
        if getattr(sys, 'frozen', False):
            import _upydev
        else:
            from . import _upydev
    except Exception as e:
        print(f'Ошибка: {e}')
    return

def fork_fun(fn,args):
    p = Process(target=fn,args=(args,))
    p.start()
    p.join()
    
def tool_telnet(*_,host:str,**kwargs):
    try:
        result = subprocess.run(['telnet',host],capture_output=False, text=True, check=True)
    except Exception as e:
        print(f'Ошибка: {e}')
    return result.stdout

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
excluded_files = '"*__pycache__*" "*/persist.*" "*/upydev_.*"'
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
        }

def main():
    parser = argparse.ArgumentParser(prog='kraxcli',description="Обертка для pyserial-ports/mpremote/upydev",add_help=True)
    parser.add_argument("--host",default=None, help='IP/хост устройства')
    parser.add_argument("--password",default='115200', help='Пароль')
    parser.add_argument("--port",default=None, help='COM-порт устройства')
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
    for x in [action_mpremote,action_upydev,action_serials,action_stop,action_repl,action_run,action_reset,action_diff,action_get,action_put,action_compare,action_check]:
        x.add_argument(
            'extra_args',
            nargs=argparse.REMAINDER,
            help="Дополнительные аргументы для передачи"
        )
    action_mpremote.set_defaults(tool=tool_mpremote)
    action_upydev.set_defaults(tool=tool_upydev)
    
    args,unknown = parser.parse_known_args()
    # настройка upydev
    
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
            action[0]( action[1] + unknown + args.extra_args,port=args.port,host=args.host )

if __name__ == "__main__":
    main()