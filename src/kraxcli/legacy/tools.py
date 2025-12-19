import sys
    
def tool_upydev(args,*_,**kwargs):
    if getattr(sys, 'frozen', False):
        upydev_path = os.path.join(sys._MEIPASS,'bin','upydev')
        os.environ['PATH'] = os.environ['PATH']+os.pathsep+os.path.join(sys._MEIPASS,'bin')
    else:
        import shutil
        import site
        import sysconfig
        os.environ['PATH'] = os.environ.get('PATH','.')+os.pathsep+os.pathsep.join([os.path.join(p,'bin') for p in site.getsitepackages()])+os.pathsep+sysconfig.get_paths()['scripts']
        
        upydev_path = shutil.which("upydev")

    # Чтение и выполнение кода
    with open(upydev_path, 'r', encoding='utf-8') as f:
        code = f.read()
        sys.argv = ['upydev']+args
        try:
            exec(code,{'__file__': upydev_path, '__name__': '__main__'})  # Эмулируем __main__
        except SystemExit:
            pass
        except:
            import traceback; traceback.print_exc();
    return

import questionary
import json
import os
from collections import Counter

def make_layout(*args, **kwargs):
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

    krax_json = { "slots":[],"devs":[],"init":{ },"devices": [ {"driver":"krax","name":"hw"},{"driver":"posto","name":"posto"} ],"node_id":1,"scanTime":100 }
    for module,size in result:
        krax_json["slots"].append(size)
        krax_json["devs"].append(module)
    
    os.mkdir('data')
    with open("data/krax.json", "w", encoding="utf-8") as f:
        json.dump(krax_json, f, ensure_ascii=False, indent=2)

    if not os.path.exists("data/krax.csv") and not os.path.exists('krax.csv'):
        with open("data/krax.csv", "w") as f:
            f.write("Имя;Тип;Модуль;Канал;Описание\n")

    if not os.path.exists("krax.py"):        
        with open("krax.py", "w") as f:
            f.writelines(["from pyplc.platform import plc, hw\n","plc.run(instances=(),ctx=globals())"])

    if not os.path.exists("project.py"):        
        with open("project.py", "w") as f:
            f.writelines(["name='БезИмени'\n","version='v0.1'"])
        
    return result
