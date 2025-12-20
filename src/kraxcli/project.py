import typer
import subprocess
import re
import tkinter as tk
import questionary
import json
import yaml
import os
from collections import Counter

app = typer.Typer(help='Работа с проектом (vars/validate/layout/)',rich_help_panel='Проект')

@app.command(help='Проверить проект на синтаксис',rich_help_panel='Проект')
def validate():
    try:
        ret = subprocess.run(['python3','krax.py','--exports'],capture_output=True,text=True)
        return ret.returncode
    except Exception as e:
        typer.secho(f'Случилось непредвиденное, {e}',bold=True,err=True)
    
@app.command(help='Получить экспортируемые переменные',rich_help_panel='Проект')
def vars(format: str = typer.Option(None,help='Формат экспорта переменных (CSV,PY,VAR_CONFIG)'),
        silent: bool = typer.Option(False,help='Скопировать в буфер и не выводить'),
        short: bool = typer.Option(False,help='Краткая информация'),
        source: str = typer.Argument(None,help='Источник переменных (если не указан то все доступные)')):
    try:
        extra=[]
        snippet=''
        if format and format.upper()=='CSV':
            extra+=['--format','CSV']
        elif format and format.upper()=='VAR_CONFIG':
            extra+=['--format','VAR_CONFIG']
        if source:
            extra+=['--export',source]
            
        ret = subprocess.run(['python3','krax.py','--exports']+extra,capture_output=True,text=True)
        format = format or 'VAR_CONFIG'
        if format.upper()=='VAR_CONFIG':
            match = re.search( 'VAR_CONFIG.*END_VAR', ret.stdout,re.DOTALL )
            if match:
                snippet=match.group(0)
        elif format.upper()=='CSV':
            lines = []
            for line in ret.stdout.split('\n'):
                if re.match(r'^\w+;.*$',line,re.DOTALL):
                    lines.append(line)
            snippet = '\n'.join(lines)
        elif format.upper()=='PY':
            fake = []
            
            for line in str(ret.stdout).split('\n'):
                line = str(line).strip()
                match = re.search(r'^([^\.]*) AT',line)
                if match:
                    fake.append(match.group(1))

            if len(fake)>0:
                snippet = (f"""
#VSCode autocompleter блок.
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from collections import namedtuple
    HW = namedtuple('HW',['{str('\',\'').join(fake)}'],defaults=[])
    hw = HW()
""")
        if snippet:
            if silent==False:
                if short:
                    typer.secho(f'Скопировано в буффер {len(snippet.split("\n"))} строк',bold=True)                    
                else:
                    typer.secho('Начало доступных данные',bold=True)
                    print(snippet)
                    typer.secho('Конец доступных данные (скопированы в буфер обмена)',bold=True)
            root = tk.Tk()
            root.withdraw()  # скрыть окно
            root.clipboard_clear()
            root.clipboard_append(snippet)
            root.update()    # важно: фиксирует данные в системном буфере
            root.destroy()

        return ret.returncode
    except Exception as e:
        typer.secho(f'Случилось непредвиденное, {e}',bold=True,err=True)

@app.command(help='Создать настройку модулей ввода-вывода (krax.json+krax.csv)',rich_help_panel='Проект')
def layout(dir: str=typer.Option('data',help='Расположение создаваемых файлов')):
    MODULES = {
        "AI-455": 8,
        "AO-555": 8,
        "DO-530": 1,
        "DI-430": 1,  # базовый размер, импульсные добавляются отдельно
        "DI-430+": 1   # базовый размер, импульсные добавляются отдельно
    }
    
    result = []

    choice = None
    while True:
        choice = questionary.select(
            "Выберите модуль для добавления:",
            choices=list(MODULES.keys()) + ["[Завершить выбор]"],default=choice
        ).ask()

        if choice == "[Завершить выбор]":
            break

        if choice == "DI-430+":
            choice = "DI-430"
            pulse_str = questionary.text("Сколько каналов в режиме импульсов?",default="1").ask()
            try:
                pulse_count = int(pulse_str)
                if pulse_count < 0:
                    print("Количество должно быть неотрицательным.")
                    continue
            except ValueError:
                print("Введите целое число.")
                continue
            size = MODULES[choice] + pulse_count
        else:
            size = MODULES[choice]

        result.append((choice, size))
        type_counts = Counter(module for module, _ in result)
        for module, count in type_counts.items():
            print(f"- {module} x {count}")

    krax_json = { "slots":[],"devs":[],"init":{ "host":"krax","iface":0 },"devices": [ {"driver":"krax","name":"hw"},{"driver":"posto","name":"posto"} ],"node_id":1,"scanTime":100 }
    for module,size in result:
        krax_json["slots"].append(size)
        krax_json["devs"].append(module)
    
    os.makedirs(dir,exist_ok=True)

    with open(f"{dir}/krax.json", "w", encoding="utf-8") as f:
        json.dump(krax_json, f, ensure_ascii=False, indent=2)

    with open(f"{dir}/krax.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(krax_json, f)

    if not os.path.exists(f"{dir}/krax.csv") and not os.path.exists('krax.csv'):
        with open("{dir}/krax.csv", "w") as f:
            f.write("Имя;Тип;Модуль;Канал;Описание\n")
        
    return result

@app.command(help='Создать минимальный проект (project.py+krax.py)')
def init(name: str=typer.Option(None,help='Название проекта'),
            version: str=typer.Option(None,help='Версия проекта'),
            force: bool=typer.Option(False,help='Затереть существующие файлы')):
    name = name or questionary.text('Как назвать проект').ask()
    version = version or questionary.text('Версия проекта').ask()
    if name=='': name = 'БезИмени'
    if version=='': version = 'v0.1'
    
    if not os.path.exists('project.py') or force:
        with open('project.py','w+t') as f:
            f.write(
f"""
name='{name}'
version='{version}'
"""
            )
    
    if not os.path.exists('krax.py') or force:
        with open('krax.py','w+t') as f:
            f.write(
"""
from pyplc.platform import plc,hw
from pyplc.utils.logging import logger
from project import name as project_name,version as project_version

logger.info(f'Запуск проекта {project_name} {project_version}')

if plc: plc.run(instances=(),ctx=globals())
"""  
            )