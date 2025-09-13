import sys
import logging
import colorlog
import argparse

from serial.tools.list_ports import main as list_serials
try:
    from telnetlib3.client import main as telnet
except:
    pass
from mpremote.main import main as mpremote
from upydev.gencommands import gen_command

def stop( serial: bool = True, target: str = None,password: str = '115200' ):
    if serial:
        logging.debug('остановка ПЛК по COM-порту')
        sys.argv = ["mpremote","soft-reset"]
        return mpremote()
    else:
        logging.debug('остановка ПЛК по IP/хосту')
        args = argparse.Namespace()
        args.m = 'kbi'
        args.t = target
        args.p = password
        args.wss = False
        return gen_command(args,[],command_line='kbi -t {target} -p {password}')

def repl( serial: bool = True, device: str = None):
    if serial:
        sys.argv = ["mpremote"]
        if device is not None: sys.argv.append(device)
        return mpremote( )
    else:
        sys.argv = ["telnetlib3-client",device]
        return telnet( )

def main():
    parser = argparse.ArgumentParser(description="krax_cli")
    parser.add_argument("--list-serials",action='store_true',default=False, help="Список доступных COM-портов")
    parser.add_argument("--repl",action='store_true',default=False, help="Подключиться к REPL ПЛК")
    parser.add_argument("--target",default=None, help='IP/хост устройства')
    parser.add_argument("--stop",default=False, action='store_true',help='Остановить выполнение программы')
    
    args,others = parser.parse_known_args()

    if args.target is None:
        serial = True
    else:
        serial = False
        
    if args.stop:
        stop(serial,args.target)
    
    if args.list_serials:
        sys.argv = ["pyserial-ports"]
        return list_serials()
    elif args.repl:
        return repl(serial,args.target)
    
if __name__ == "__main__":
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s — %(levelname)-8s — %(message)s",
        log_colors={
            "DEBUG":    "cyan",
            "INFO":     "green",
            "WARNING":  "yellow",
            "ERROR":    "red",
            "CRITICAL": "bold_red",
        },
        datefmt="%H:%M:%S"
    ))

    logger = colorlog.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    main()
