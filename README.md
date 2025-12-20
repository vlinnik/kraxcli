# Введение
Обертка для утилит pyserial-ports/mpremote/upydev для работы с KRAX

в Windows установка pyserial/upydev/mpremote требует установленной visual studio. 
Чтобы обойти это для windows можно создать с помощью pyinstaller krax_cli.exe, 
в котором все утилиты уже собраны.

# Сборка

## pyinstaller

для сборки exe нужно:
установить в venv (у меня .venv) 
- pyserial
- mpremote
- upydev
- pyinstaller
- questionary
- typer

затем активировать venv и там
```bash
. .venv/bin/activate
pyinstaller kraxcli.spec --noconfirm
deactivate
```

## debian

Если нет каталога debian
```
dh_make -n --python -p kraxcli_0.1 -e vlinnik@mail.ru 
```
Убрать из debian/control генерацию doc 
```
debuild -uc -us
```