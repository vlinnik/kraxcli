import typer
import os
from cli import upydev

app = typer.Typer(help='Настройка параметров подключения')
# Подкоманда connect
@app.callback(invoke_without_command=True)
def connect(
    host: str = typer.Option(None, "-h", "--host", help="Хост для подключения"),
    password: str = typer.Option('115200', "--password", help="Пароль (хранится явно)"),
    port: str = typer.Option(None, "-p", "--port", help="Хост для подключения"),
):
    if port:
        typer.echo(f'Настройка подключения к {port} baudrate 115200')
        upydev('config','-t',port,'-p','115200','-@','usbdev')
    elif host:
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
    typer.echo('Информация о подключенном контроллере:')
    upydev('info')