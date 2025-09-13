Обертка для утилит pyserial-ports/mpremote/upydev для работы с KRAX

для сборки exe нужно:
установить в venv (у меня .venv) 
pyserial, mpremote,upydev,pyinstaller

затем активировать venv и там
```
pyinstaller krax_cli.spec --noconfirm
```
