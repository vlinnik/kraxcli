.. kraxcli tool documentation master file, created by
   sphinx-quickstart on Sun Dec 21 10:11:45 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Утилита для работы с KRAX PLC kraxcli
=====================================

Документ описывает использование утилиты kraxcli из командной строки для решения 
основных повседневных задач при работе с контроллером KRAX PLC-932

Утилита является оболочкой для python утилит и модулей: mpremote, upydev, pyserial.
Командами и параметрами оболочка выбирает какую запустить утилиту и ее параметры.

Цели утилиты: собрать все в один установочный пакет или исполнительный файл, чтобы 
его было удобно использовать из VSCode, устанавливать в Windows и обеспечить абстракцию
от используемых утилит (например если захочется применить rshell+telnet) 

.. toctree::
   :maxdepth: 2
   :caption: Содержание:

   install
   usage
   commands
