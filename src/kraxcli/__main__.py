import typer
import sys
import os
from _version import __version__
from .connect import app as connect
from cli import detect_type,upydev, mpremote,telnet
from typing import List

excluded_files = '"*__pycache__*" "*/persist.*" "*/upydev_.*" "micropython.py" "webrepl_cfg.py" "*/.git/*"'
app = typer.Typer(chain=True)
cwd = os.curdir

# Глобальный флаг
@app.callback(invoke_without_command=True)
def main(
    w: str = typer.Option(
        None,
        "-w",
        "--root",
        help="Расположение проекта"
    ),
    version: bool = typer.Option( False, "--version", help="Показать версию утилиты и выйти" )
):
    if version:
        typer.echo(f"Версия kraxcli {__version__}")
        exit(0)
    if w:
        os.chdir(w)

@app.command(help='Проверить проект на синтаксис')
def recheck():
    pass

@app.command(help='Показать список доступных последовательных портов')
def serials():
    from serial.tools import list_ports
    sys.argv = ['pyserial-ports','-q','(USB|COM|ACM)']
    ports = list_ports.main()  # Вызываем функцию main из list_ports
    return ports

@app.command(help='Остановить выполнение программы')
def stop(silent:bool = typer.Option(False,help='Работать по тихому')):
    if silent==False: typer.echo('Останов программы в контроллере...')
    if detect_type()=='serial' and silent==False:
        mpremote('soft-reset')
    else:
        upydev('kbi')

@app.command(help='Перезапуск контроллера')
def reset():
    typer.echo('Перезапуск контроллера...')
    if detect_type()=='serial':
        mpremote('reset')
    else:
        upydev('reset')

@app.command(help='Подключиться к REPL')
def repl():
    if detect_type()=='serial':
        mpremote()
    else:
        if sys.platform=='linux':
            upydev('repl')
        else:
            typer.echo('Запуск внешней утилиты telnet. Пользователь по умолчанию micro/115200')
            telnet()
            
@app.command('upydev',help='Запуск upydev')
def _upydev(args: List[str] = typer.Argument(...)):
    upydev(*args)

@app.command('mpremote',help='Запуск mpremote')
def _mpremote(args: List[str] = typer.Argument(...)):
    mpremote(*args)

def __check_upydev():
    if not os.path.exists('upydev_.config'):
        typer.echo('Необходимо произвезти настройку (комманда connect)',err=True)
        exit(0)
    
@app.command(help='Структура файловой системы')
def tree():
    if os.path.exists('upydev_.config'):
        upydev('tree')
    else:
        mpremote('tree')
        
@app.command(help='Показать различия контроллер<->проект')
def diff():
    __check_upydev()
    typer.echo('Показать разницу проекта с контроллером...')
    upydev(*['dsync','-fg','-n','-p','-i',excluded_files])

@app.command(help='Сравнить контроллер<->проект')
def compare():
    __check_upydev()
    typer.echo('Сравнение проекта с контроллером...')
    upydev(*['dsync','-fg','-n','-i',excluded_files])

@app.command(help='Запуск программы в контроллере')        
def run(script: str = typer.Argument('krax')):
    __check_upydev()
    typer.echo(f'Запуск в контроллере файла {script}...')
    upydev('run',script)

@app.command(help='Скачать проект из контроллера')
def get(
    file: str=typer.Argument(None,help='Файл(ы) для скачивания'),
    dir: str=typer.Option(None,'-d','--dir',help='Каталог откуда скачивать'),
    ):
    __check_upydev()
    if file:
        typer.echo(f'Скачивание файла(ов) {file} из контроллера')
        extra = []
        if dir:
            extra+=['-dir',dir]
        extra.append(file)
        upydev('get','-fg',*extra)
    else:
        typer.echo(f"Скачиваем проект из контроллера..")
        upydev('dsync','-d','-fg','-i',excluded_files)

@app.command(help='Закачать проект в контроллер')
def put(file: str=typer.Argument(None,help='Что отправить, или все файлы если не указано'),
        dir: str=typer.Option(None,'-d','--dir',help='Каталог куда отправить'),
        reset: bool = typer.Option(False,help='Мягкий перезапуск после загрузки')
        ):
    __check_upydev()
    if file: 
        typer.echo(f'Запись файла {file} в контроллер')
        extra = []
        if dir:
            extra+=['-dir',dir]
        if reset: extra.append('-rst')
        extra.append(file)
        upydev('put','-fg','-i',excluded_files,*extra)
    else:
        typer.echo(f'Запись проекта в контроллер')
        upydev('dsync','-fg','-i',excluded_files)

@app.command(help='Отправить файл в контроллер и выполнить')
def load(file: str=typer.Argument(...,help='Что отправить')):
    __check_upydev()
    upydev('load',file)

@app.command(help='Отправить файл в контроллер и выполнить')
def shl():
    if sys.platform!='linux':
        typer.secho('Жаль cmd/powershell-подобная среда доступна только в linux',bold=True)
        return
    __check_upydev()
    stop(silent=True)
    upydev('shl')

@app.command(help='Проверить содержимое project.py')
def check():
    __check_upydev()
    typer.echo('Вывод содержимого project.py')
    stop(silent=True)
    upydev('cat','project.py')  
    
@app.command(help='Удалить файл(ы) из контроллера')
def rm( file: str=typer.Argument(...,help='Имя/шаблон файла')):
    __check_upydev()
    typer.echo(f'Удалить файл(ы) {file} из контроллера')
    upydev('rm','-rf',file)

@app.command(help='Список файлов')
def ls( file: str=typer.Argument('.',help='Имя/шаблон файла')):
    if detect_type()=='serial':
        mpremote('ls',file)
    else:
        upydev('ls',file)

if __name__ == "__main__":
    if 'HOME' not in os.environ:
        current_dir = os.getcwd()
        os.environ['HOME'] = current_dir
        
    app.command('upload',help='Записать файл в контроллер')(put)
    app.command('download',help='Скачать файл из контроллера')(get)
    app.add_typer(connect,name='connect',invoke_without_command=True)
    app.add_typer(connect,name='config',invoke_without_command=True)
    app()
