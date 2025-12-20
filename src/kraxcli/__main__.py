import typer
import sys
import os
from kraxcli._version import __version__
from kraxcli.connect import app as connect
from kraxcli import detect_type,upydev, mpremote,telnet
from typing import List
import kraxcli.files as files
import kraxcli.device as device
import kraxcli.project as project

excluded_files = '"*__pycache__*" "*/persist.*" "*/upydev_.*" "micropython.py" "webrepl_cfg.py" "*/.git/*"'
app = typer.Typer(chain=True)
cwd = os.curdir

# Глобальный флаг
@app.callback(invoke_without_command=True)
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
        os.chdir(w)
            
@app.command('upydev',help='Запуск upydev (USB/Ethernet подключение)',rich_help_panel='Инструменты')
def _upydev(args: List[str] = typer.Argument(...)):
    upydev(*args)

@app.command('mpremote',help='Запуск mpremote (USB подключение)',rich_help_panel='Инструменты')
def _mpremote(args: List[str] = typer.Argument(...)):
    mpremote(*args)

def __check_upydev():
    if not os.path.exists('upydev_.config'):
        typer.echo('Необходимо произвезти настройку (комманда connect)',err=True)
        exit(0)
        
def cli():
    if 'HOME' not in os.environ:
        current_dir = os.getcwd()
        os.environ['HOME'] = current_dir
    
    app.registered_commands+=files.app.registered_commands
    app.registered_commands+=device.app.registered_commands
    app.registered_commands+=project.app.registered_commands
            
    app.add_typer(connect,name='connect',invoke_without_command=True)
    app.add_typer(connect,name='config',invoke_without_command=True,hidden=True)
    app()

if __name__ == "__main__":
    cli()