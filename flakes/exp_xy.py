from pygame import image
from dataclasses import dataclass


@dataclass
class ExplXY:
    x: float
    y: float
    img: image
    vector_x: float
    vector_y: float
    angle: int
