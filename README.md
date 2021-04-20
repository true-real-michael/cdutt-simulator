# cdutt-simulator

Эта программа позволяет сталкивать боты для "Цирка"

Зависимости
-----------

1. Python 3 (тестировано на 3.7) (рекомендуемые версии 3.3-3.7)
2. Библиотека wexpect (устанавливается командой: ```pip install wexpect```)



Запуск
------
В директории вместе с simulator.py должны находиться файлы ботов команд: team0.exe и team1.exe

В cmd, открытой в директории запустить файл командой ```python simulator.py```

Программа будет выводить состояние доски и счет команд


Настройки
---------

Программа также подерживает:
1. ручую игру за одну или обе команд
2. измененное количество ходов
3. Заданный вручную набор домов

Для этого нужно отредактировать соответствующие переменные в *config.py*
![image](https://user-images.githubusercontent.com/64229743/115419128-bed20000-a202-11eb-80d3-5a545b54df4f.png)
