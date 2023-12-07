import pygame
from math import sin, cos
from random import randint, choice
from flakes.exp_xy import ExplXY
from flakes.snowflake import SnowFlake

"""
    Класс для обработки эффектов при клике на подарок. Содержит в себе все изображения
    разлетающихся подарков.
"""


class GiftExplose:
    # Вектора движения для изображений вокруг координат клика
    vx = [0, 60, 75, 0, -75, -60, -30]
    vy = [-130, -200, -150, -220, -150, -200, -100]
    img = pygame.image.load("images/others/gift.png")

    def __init__(self, x, y, sounds):
        sounds.play_gift()
        self.frame = 0

        # Изменит размер изображения в соответствии с пропорциями и размером экрана
        w, h = GiftExplose.img.get_width(), GiftExplose.img.get_height()
        scale = (SnowFlake.HEIGHT / SnowFlake.WIDTH) / 4
        current_img = pygame.transform.scale(GiftExplose.img, (w * scale, h * scale))

        self.img_list = []
        for i in range(26):
            self.img_list.append(ExplXY(
                x=x + randint(-250, 250) * sin(i * 15),
                y=y + randint(-250, 250) * cos(i * 15),
                img=current_img,
                vector_x=GiftExplose.vx[i % len(GiftExplose.vx)] / 2 * randint(4, 8),
                vector_y=GiftExplose.vy[i % len(GiftExplose.vy)] / 2 * randint(4, 8),
                angle=0
            ))
            self.img_list[i].angle = 30 if self.img_list[i].vector_x > 0 else -30

        self.enabled = True

    def draw(self, scene):
        if not self.enabled:
            return

        self.frame += 1

        count = 8
        for pict in self.img_list:
            if self.frame > count * 2:
                rotated_image = pygame.transform.rotate(pict.img, -pict.angle)
                pict.rect = rotated_image.get_rect(center=pict.img.get_rect(topleft=(pict.x, pict.y)).center)
                scene.blit(rotated_image, pict.rect)
            count += 1

    def act(self, deltatime):
        if not self.enabled:
            return

        over_screen = True
        for pict in self.img_list:

            if abs(pict.vector_x) > 0.1:
                pict.vector_x *= 0.99999
                if pict.angle > 0:
                    pict.angle += pict.vector_x * deltatime * 2
                else:
                    pict.angle -= -pict.vector_x * deltatime * 2

            pict.vector_y += SnowFlake.HEIGHT * 0.45 * deltatime

            pict.x += pict.vector_x * deltatime
            pict.y += pict.vector_y * deltatime // 3

            over_screen &= pict.y > SnowFlake.HEIGHT

            # if pict.y > SnowFlake.HEIGHT - pict.img.get_height():
            #     pict.vector_y *= -0.5
            #     pict.y += pict.vector_y * deltatime

        if over_screen:
            self.enabled = False
