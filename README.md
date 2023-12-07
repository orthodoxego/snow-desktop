# Снег на рабочем столе

Играбельная "экранная заставка". Цель - выбить как можно больше снежинок, кликая в их центр. Можно использовать как аим-тренажёр :)

После 30 секунд игры и 15 закликанных снежинок в правом верхнем углу появляется скорость: количество выбитых в минуту.

Можно и не играть, конечно, тогда снег продолжит падать и создавать примитивный png-сугроб, это прорыв.

Для удаления рекорда достаточно удалить файл record.dat

### Управление:
- мышь

### Особенности:
Если кликнуть вне игровых объектов, то Windows переключается на другую рабочую область, следующий клик не будет засчитан (произойдёт переключение на игровую область игры).

### Библиотеки:
В случае отсутствия необходимых библиотек, следует выполнить в командной строке:
* pip install pygame
* pip install pywin32
* pip install pyautogui

Программа запускается файлом <b>snow-desktop.py</b>.
***
Настройки можно изменить в <b>snow-desktop.py</b>:
````
FPS = 60                    # Изменить, чтобы увеличить/уменьшить ФПС
max_flakes = 300            # Макс. кол-во снежинок
max_gifts = 1               # Макс. количество подарков на экране
````
***

Экспериментируйте, изменяйте, играйте, всем добра!
