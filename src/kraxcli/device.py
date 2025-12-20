import typer
import sys
import os
from kraxcli import detect_type,upydev, mpremote,telnet

app = typer.Typer(chain=True,rich_help_panel='Контроллер')

def __check_upydev():
    if not os.path.exists('upydev_.config'):
        typer.echo('Необходимо произвести настройку (команда connect)',err=True)
        exit(0)

@app.command(help='Показать список доступных последовательных портов',rich_help_panel='Контроллер',)
def serials():
    from serial.tools import list_ports
    sys.argv = ['pyserial-ports','-q','(USB|COM|ACM)']
    ports = list_ports.main()  # Вызываем функцию main из list_ports
    return ports

@app.command(help='Перезапуск контроллера',rich_help_panel='Контроллер')
def reset():
    typer.echo('Перезапуск контроллера...')
    if detect_type()=='serial':
        mpremote('reset')
    else:
        upydev('reset')

@app.command(help='Остановить выполнение программы',rich_help_panel='Контроллер')
def stop(silent:bool = typer.Option(False,help='Работать по тихому')):
    if silent==False: typer.echo('Останов программы в контроллере...')
    if detect_type()=='serial' and silent==False:
        mpremote('soft-reset')
    else:
        upydev('kbi')

@app.command(help='Запуск программы в контроллере',rich_help_panel='Контроллер')        
def run(script: str = typer.Argument('krax')):
    __check_upydev()
    typer.echo(f'Запуск в контроллере файла {script}...')
    upydev('run',script)

@app.command(help='Подключиться к REPL',rich_help_panel='Контроллер')
def repl():
    if detect_type()=='serial':
        mpremote()
    else:
        if sys.platform=='linux':
            upydev('repl')
        else:
            typer.echo('Запуск внешней утилиты telnet. Пользователь по умолчанию micro/115200')
            telnet()

@app.command(help='Отправить файл в контроллер и выполнить',rich_help_panel='Контроллер')
def load(file: str=typer.Argument(...,help='Что отправить')):
    __check_upydev()
    upydev('load',file)

@app.command(help='Режим командной строки',rich_help_panel='Контроллер')
def shl():
    if sys.platform!='linux':
        typer.secho('Жаль cmd/powershell-подобная среда доступна только в linux',bold=True)
        return
    __check_upydev()
    stop(silent=True)
    upydev('shl')

@app.command(help='Проверить содержимое project.py',rich_help_panel='Контроллер')
def check():
    __check_upydev()
    typer.echo('Вывод содержимого project.py')
    stop(silent=True)
    upydev('cat','project.py')  
