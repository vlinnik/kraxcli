Установка
=========

Способы установки

PyPI
----

Пока не загружено на PyPI, можно установить напрямую whl:

.. code-block:: bash

    pip install kraxcli-<версия>.whl


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

Скопировать kraxcli.exe в папку из PATH, например C:\Windows\System32

Создание бинарного пакета из исходников
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Перед созданием бинарного пакета необходимо настроить venv, и установить в ней все зависимости:

.. code-block:: bash

    python -m venv .venv
    source .venv/bin/activate      # Linux
    pip install -r requirements.txt
    pip install pyinstaller
    pyinstaller kraxcli.spec

После этого в папке dist/ будет находиться исполняемый файл kraxcli.

.. note::

    Во время сборки появятся ошибки вида:
    ::

        site-packages/upydev/bleio.py:402: SyntaxWarning: invalid escape sequence '\.'
        site-packages/upydev/serialio.py:395: SyntaxWarning: invalid escape sequence '\.'
        site-packages/upydev/wsio.py:785: SyntaxWarning: invalid escape sequence '\.'
        
    Можно проигнорировать, или исправить в исходниках upydev, заменив на '\\\\.'

Требования
----------
Python 3.8+; см. pyproject.toml для деталей.
Платформы: Linux, Windows, macOS.

Пользователь должен иметь права на доступ к последовательным портам (обычно это группа dialout на Linux).