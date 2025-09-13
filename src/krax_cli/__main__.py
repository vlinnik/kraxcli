import subprocess
import sys
import argparse
from serial.tools import list_ports

def run_command(command, args):
    """Запускает указанную команду с переданными аргументами."""
    try:
        if command == "pyserial-ports":
            sys.argv = [command]+args+['-q','(USB|COM|ACM)']
            ports = list_ports.main()  # Вызываем функцию main из list_ports
            return ports
        if command == "upydev":
            sys.argv = [command]+args
            import _upydev
            return
        if command == "mpremote":
            sys.argv = [command]+args
            from mpremote import __main__
            return
        else:
            # Для других команд (например, mpremote) вызываем напрямую
            cmd = [command] + args
        result = subprocess.run(cmd, capture_output=False, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении {command}: {e.stderr}")
        return None
    except FileNotFoundError:
        print(f"Ошибка: {command} не найден. Убедитесь, что {command} установлен.")
        return None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None
        
    
def main():
    parser = argparse.ArgumentParser(description="Wrapper для pyserial-ports и mpremote",add_help=True)
    parser.add_argument('command', choices=['pyserial-ports', 'mpremote','upydev'], help="Команда для запуска: pyserial-ports или mpremote")

    parser.add_argument(
        'extra_args',
        nargs=argparse.REMAINDER,
        help="Дополнительные аргументы для передачи в pyserial-ports/mpremote/upydev"
    )
    
    args = parser.parse_args()
    run_command(args.command,args.extra_args)

if __name__ == "__main__":
    main()