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
dh_make -n --python -p kraxcli_0.6 -e vlinnik@mail.ru 
```

Убрать из debian/control генерацию doc и добавить  build-depends от dh-virtualenv
debian/rules изменить на dh $@ --with python-virtualenv (или надо будет ставить upydev 
postinst) и добавить (что-то там с compat=12)
```
override_dh_auto_configure:
    # ничего не делаем, шаг не нужен
```

создать файл debian/kraxcli.install
```
kraxcli usr/bin
```

Сборка deb
```
debuild -uc -us
```

Генератор debian/changelog c помощью
```
EMAIL=vlinnik@mail.ru gbp dch --debian-branch=main --release
```