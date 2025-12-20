import typer
import os
from kraxcli import upydev,detect_type,mpremote

app = typer.Typer(chain=True,help='Работа с файлами (put/get/ls/rm/tree/diff/compare)',rich_help_panel='Файлы')
excluded_files = '"*__pycache__*" "*/persist.*" "*/upydev_.*" "micropython.py" "webrepl_cfg.py" "*/.git/*"'

def __check_upydev():
    if not os.path.exists('upydev_.config'):
        typer.echo('Необходимо произвести настройку (команда connect)',err=True)
        exit(0)

@app.command(help='Скачать проект из контроллера',rich_help_panel='Файлы')
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

@app.command(help='Закачать проект в контроллер',rich_help_panel='Файлы')
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

@app.command(help='Список файлов',rich_help_panel='Файлы')
def ls( file: str=typer.Argument('.',help='Имя/шаблон файла')):
    if detect_type()=='serial':
        mpremote('ls',file)
    else:
        upydev('ls',file)

@app.command(help='Удалить файл(ы) из контроллера',rich_help_panel='Файлы')
def rm( file: str=typer.Argument(...,help='Имя/шаблон файла')):
    __check_upydev()
    typer.echo(f'Удалить файл(ы) {file} из контроллера')
    upydev('rm','-rf',file)

@app.command(help='Структура файловой системы',rich_help_panel='Файлы')
def tree():
    if os.path.exists('upydev_.config'):
        upydev('tree')
    else:
        mpremote('tree')
        
@app.command(help='Показать различия контроллер<->проект',rich_help_panel='Файлы')
def diff():
    __check_upydev()
    typer.echo('Показать разницу проекта с контроллером...')
    upydev(*['dsync','-fg','-n','-p','-i',excluded_files])

@app.command(help='Сравнить контроллер<->проект',rich_help_panel='Файлы')
def compare():
    __check_upydev()
    typer.echo('Сравнение проекта с контроллером...')
    upydev(*['dsync','-fg','-n','-i',excluded_files])
