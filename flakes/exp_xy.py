from pygame import image
from dataclasses import dataclass


"""
    Класс для хранения данных об объекте-анимации при нажатии на снежинку/подарок
"""
@dataclass
class ExplXY:
    x: float            # Координата X
    y: float            # Координата Y
    img: image          # Изображение png
    vector_x: float     # Вектор движения по X
    vector_y: float     # Вектор движения по Y
    angle: int          # Угол поворота фигуры
