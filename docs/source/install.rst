Установка
=========

Способы установки: PyPI, deb-пакет, бинарный (PyInstaller), из исходников

Требования
----------

::

    Python 3.8+; см. pyproject.toml для деталей.
    Платформы: Linux, Windows, macOS.

Windows
~~~~~~~
- Сборка из исходников: Visual Studio Community Edition с компонентами для разработки на C++

.. attention::

    Рекомендуется использовать бинарный пакет

Linux
~~~~~

- Права на доступ к последовательным портам (обычно это группа dialout на Linux).
- Установленный python3-tk

.. code-block:: bash

    sudo apt install python3-tk

- Для сборки из исходников необходим gcc: 

.. code-block:: bash

    sudo apt install gcc

PyPI
----

Пока не загружено на PyPI, можно установить напрямую whl:

.. code-block:: bash

    pip install kraxcli-<версия>.whl

.. note:: 

    Для Linux необходимы python3-tk, gcc (Debian: sudo apt install python3-tk gcc)


Из исходников
-------------
.. code-block:: bash

    git clone https://vlinnik/kraxcli.git && cd kraxcli && pip install .

Из debian-пакета
----------------
.. code-block:: bash

    sudo apt install kraxcli-<версия>.deb

Бинарный пакет (сделан с pyinstaller)
-------------------------------------

Linux
~~~~~

Скопировать kraxcli в /usr/bin (для vscode /usr/local/bin не сработать может)

.. code-block:: bash

    sudo cp kraxcli /usr/bin/kraxcli
    sudo chmod +x /usr/bin/kraxcli

Windows
~~~~~~~

Скопировать kraxcli.exe в папку из PATH, например C:\\Windows\\System32

Создание бинарного пакета из исходников
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Перед созданием бинарного пакета необходимо настроить venv, и установить в ней все зависимости:

.. code-block:: bash

    python -m venv .venv
    source .venv/bin/activate      # Linux
    pip install -r requirements.txt
    pip install pyinstaller

.. note:: 

    Для Linux необходимо установить пакет python3-tk, gcc (Debian: sudo apt install python3-tk gcc)

.. code-block:: bash

    pyinstaller kraxcli.spec

.. attention::

    для Windows нужно изменить структуру папок в .venv/Lib/site-packages 
    на Lib/python<версия>/site-packages, иначе pyinstaller не сможет найти зависимости upydev.
    <версия> - это основная и второстепенная версия Python, например 3.8. Можно узнать запустив 
    pyinstaller и посмотрев на ошибки.


После этого в папке dist/ будет находиться исполняемый файл kraxcli.

.. note::

    Во время сборки появятся ошибки вида:
    ::

        site-packages/upydev/bleio.py:402: SyntaxWarning: invalid escape sequence '\.'
        site-packages/upydev/serialio.py:395: SyntaxWarning: invalid escape sequence '\.'
        site-packages/upydev/wsio.py:785: SyntaxWarning: invalid escape sequence '\.'
        
    Можно проигнорировать, или исправить в исходниках upydev, заменив на '\\\\.'
