Быстрый старт
=============

Перед использованием нужно настроить подключение к устройству. 
Настройка сохраняется в каталоге проекта (рабочий каталог).
Далее можно использовать выбор рабочего каталога с помощью опции -w.

Показать справку:

.. code-block:: bash    

    kraxcli --help

Разберем на примере создания проекта demo для поддержания уровня в баке.
Проект контроллера будет находиться в папке demo/src/plc.

Пример
------

Создадим проект demo с модулями AI-455, DI-430, DO-530:

.. code-block:: bash    

    mkdir -p demo/src/plc
    kraxcli -w ./demo/src/plc/ project init --name demo --version v0.1
    kraxcli -w ./demo/src/plc/ project layout --dir data
    ? Выберите модуль для добавления: AI-455
    - AI-455 x 1
    ? Выберите модуль для добавления: DI-430
    - AI-455 x 1
    - DI-430 x 1
    ? Выберите модуль для добавления: DO-530
    - AI-455 x 1
    - DI-430 x 1
    - DO-530 x 1
    ? [Завершить выбор]

После последней команды в папке demo/src/plc/data появится файл krax.csv, изменим его чтобы получилось:

.. code-block:: none

    Имя;Тип;Модуль;Канал;Описание

    LEVEL;AI;1;1;Уровень жидкости в баке
    ISON;DI;2;1;Состояние насоса
    PUMP;DO;3;1;Насос подачи жидкости    

Теперь скопируем в буфур обмена описание переменных для autocomplete в VSCode:

.. code-block:: bash

    kraxcli -w ./demo/src/plc/ project vars --format PY --short

Изменим скрипт demo/src/plc/krax.py чтобы получилось:

.. code-block:: python

    from pyplc.platform import plc,hw
    from pyplc.utils.logging import logger
    from project import name as project_name,version as project_version

    logger.info(f'Запуск проекта {project_name} {project_version}')

    #VSCode autocompleter блок.
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from collections import namedtuple
        HW = namedtuple('HW',['LEVEL','ISON','PUMP'],defaults=[])
        hw = HW()
    #Конец блока.

    def prg():
        #Пример программы управления насосом по уровню жидкости в баке.
        LEVEL_THRESHOLD = 32767  #Порог уровня для включения насоса

        if hw.LEVEL < LEVEL_THRESHOLD and not hw.PUMP:
            hw.PUMP = True   #Включение насоса
            logger.info('Насос включен')

        if hw.LEVEL >= LEVEL_THRESHOLD and hw.PUMP:        
            hw.PUMP = False  #Выключение насоса
            logger.info('Насос выключен')
                    
    if plc: plc.run(instances=( prg , ),ctx=globals())

Участок кода с комментарием "VSCode autocompleter блок" нужен только для автодополнения в VSCode и не влияет на работу программы. Его вставляем из
буфера обмена. Функция prg реализует простое управление насосом по уровню жидкости в баке.

Теперь настроим подключение к устройству (контроллеру с MicroPython и pyplc-библиотекой):

.. code-block:: bash    

    kraxcli -w demo/src/plc dev connect /dev/ttyUSB0 check

Должно получиться что-то вроде:

.. code-block:: none

    Настройка подключения к /dev/ttyUSB0 baudrate 115200
    SerialDevice usbdev settings saved in working directory!
    Информация о подключенном контроллере:
    SerialDevice @ /dev/ttyUSB0, Type: esp32, Class: SerialDevice
    Firmware: MicroPython v1.26.0-preview.460.g88cb6bc81.dirty on 2025-12-11; PYPLC module (spiram) with ESP32
    CP2104 USB to UART Bridge Controller, Manufacturer: Silicon Labs
    (MAC: 78:e3:6d:74:9b:14)

Отправить проект в контроллер и запустить его:


.. code-block:: bash

    kraxcli -w demo/src/plc fs put
    kraxcli -w demo/src/plc dev run

После этого в консоли контроллера должны появиться сообщения о запуске проекта и управлении насосом:

::

    Запуск в контроллере файла krax...
    Running krax...

    PYPLC:          0.3.0.post54+g609f14b9e.d20251220
    Платформа:      esp32
    
    ⚠  INFO    Запуск подсистемы обмена с устройствами
    ➤  DEBUG   инициализация pyplc-платформы
    ➤  DEBUG   Использованы настройки из data/krax.json
    ⚠  INFO    Подключен драйвер modbus.slave, реализация Publisher
    ⚠  INFO    Подключен драйвер krax, реализация KRAX
    ⚠  INFO    Подключен драйвер posto, реализация Publisher
    ✔  WARNING Подключить драйвер modbus.master неудалось: no module named 'pyModbusTCP'
    ⚠  INFO    Запуск проекта demo v0.1
    ⚠  INFO    Запуск устройства: KRAX(name='hw',slots=[8, 1, 1],size=10)
    ⚠  INFO    Запуск устройства: Publisher(name="posto")
    ⚠  INFO    Насос включен

Когда уровень жидкости превысит порог, должно появиться сообщение:

::

    ⚠  INFO    Насос выключен

Остановить выполнение программы в контроллере можно сочетанием клавиш Ctrl+C в консоли контроллера

.. note::

    Темперь можно добавить гистерезис и защиту от частых переключений.
    Программу управления почти в этом виде создает ИИ агент copilot (помощник в VSCode).

Создание проекта и настройка устройств 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash    

    kraxcli -w . project init 
    kraxcli -w . project layout --dir data 

Настроить подключение к устройству
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash    

    kraxcli -w . dev connect /dev/ttyUSB0 check

Получится что-то вроде:

.. code-block:: none

    SerialDevice @ /dev/ttyUSB0, Type: esp32, Class: SerialDevice
    Firmware: MicroPython v1.26.0-preview.460.g88cb6bc81.dirty on 2025-12-11; PYPLC module (spiram) with ESP32
    CP2104 USB to UART Bridge Controller, Manufacturer: Silicon Labs
    (MAC: 78:e3:6d:74:9b:14)

Отправить проект на устройство
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash    

    kraxcli -w . dev put

Запустить проект на устройстве
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash    

    kraxcli -w . dev run
