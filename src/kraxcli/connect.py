import typer
import os
from kraxcli import upydev
from serial.tools import list_ports

app = typer.Typer(help='Настройка параметров подключения',rich_help_panel='Контроллер',invoke_without_command=True)
# Подкоманда connect
@app.callback(invoke_without_command=True,rich_help_panel='Контроллер')
def connect(
    host: str = typer.Argument(None, help="Хост для подключения/порт"),
    password: str = typer.Option('115200', "-p","--password", help="Пароль (хранится явно)")
):
    if host is not None:
        for p in list_ports.comports():
            if p.device == host:
                typer.echo(f'Настройка подключения к {host} baudrate 115200')
                upydev('config','-t',host,'-p','115200','-@','usbdev')
                break
        else:
            typer.echo(f'Настройка подключения к {host} с паролем {password}')
            upydev('config','-t',host,'-p',password,'-@','netdev')

def __check_upydev():
    if not os.path.exists('upydev_.config'):
        typer.echo('Необходимо произвезти настройку (комманда connect)',err=True)
        return False
    return True
        
@app.command(help='Проверить соединение')
def check():
    if not __check_upydev():
        typer.echo('Подключение не настроено')
        return
    typer.secho('Информация о подключенном контроллере:',bold=True)
    upydev('info')