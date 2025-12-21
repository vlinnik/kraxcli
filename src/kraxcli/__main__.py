import typer
import sys
import os
from typing import List
import kraxcli.files as files
import kraxcli.device as device
import kraxcli.project as project
import kraxcli.connect as connect
from kraxcli._version import __version__
from kraxcli import upydev, mpremote

app = typer.Typer(chain=True)

# Глобальный флаг
@app.callback(invoke_without_command=True,no_args_is_help=True)
def main(
    w: str = typer.Option(
        None,
        "-w",
        "--root","--dev",
        help="Расположение проекта"
    ),
    version: bool = typer.Option( False, "--version", help="Показать версию утилиты и выйти" )
):
    if version:
        typer.echo(f"Версия kraxcli {__version__}")
        sys.exit(0)
    if w:
        try:
            if not os.path.exists(w):
                os.makedirs(w)
            os.chdir(w)
        except:
            typer.secho('Не удалось установить рабочий каталог',err=True)
            sys.exit(0)
            
@app.command('upydev',help='Запуск upydev (USB/Ethernet подключение)',rich_help_panel='Инструменты')
def _upydev(args: List[str] = typer.Argument(None)):
    upydev(*args)

@app.command('mpremote',help='Запуск mpremote (USB подключение)',rich_help_panel='Инструменты')
def _mpremote(args: List[str] = typer.Argument(None)):
    mpremote(*args)

def __check_upydev():
    if not os.path.exists('upydev_.config'):
        typer.echo('Необходимо произвезти настройку (комманда connect)',err=True)
        exit(0)
        
def cli():
    if 'HOME' not in os.environ:
        current_dir = os.getcwd()
        os.environ['HOME'] = current_dir
    os.environ['PATH'] = os.environ.get('PATH','')
    
    app.add_typer(device.app,name='dev')
    app.add_typer(project.app,name='project')            
    app.add_typer(files.app,name='fs')
    app()

if __name__ == "__main__":
    cli()