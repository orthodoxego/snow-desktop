import pygame
from math import sin, cos
from random import randint, choice
from flakes.exp_xy import ExplXY
from flakes.snowflake import SnowFlake


class SnowExplose:
    image_files = None
    vx = [0, 60, 75, 0, -75, -60]
    vy = [-130, -200, -150, -220, -150, -200]

    @staticmethod
    def get_images():
        ret = []
        imgs = [pygame.image.load("images/others/expl01.png"),
                pygame.image.load("images/others/expl02.png"),
                pygame.image.load("images/others/expl03.png"),
                pygame.image.load("images/others/expl04.png"),
                pygame.image.load("images/others/expl05.png"),
                pygame.image.load("images/others/expl06.png")]

        scale = (SnowFlake.HEIGHT / SnowFlake.WIDTH) / 1.8

        for pct in imgs:
            w, h = pct.get_width(), pct.get_height()
            ret.append(pygame.transform.scale(pct, (w * scale, h * scale)))

        return ret

    def __init__(self, x, y, sounds):
        if SnowExplose.image_files is None:
            SnowExplose.image_files = SnowExplose.get_images()

        sounds.play_expl()

        self.img_list = []
        for i in range(6):
            self.img_list.append(ExplXY(
                x=x + randint(5, 10) * sin(i * 45),
                y=y + randint(5, 10) * cos(i * 45),
                img=choice(SnowExplose.image_files),  # SnowExplose.image_files[i],
                vector_x=SnowExplose.vx[i] * randint(2, 4) + randint(-100, 100),
                vector_y=SnowExplose.vy[i] * randint(2, 4),
                angle=0
            ))
            self.img_list[i].angle = 30 if self.img_list[i].vector_x > 0 else -30

        for i in range(6):
            self.img_list.append(ExplXY(
                x=x + randint(15, 30) * sin(i * 45),
                y=y + randint(15, 30) * cos(i * 45),
                img=choice(SnowExplose.image_files),  # SnowExplose.image_files[i],
                vector_x=SnowExplose.vx[i] * randint(4, 6) + randint(-100, 100),
                vector_y=SnowExplose.vy[i] * randint(1, 5),
                angle=0
            ))
            self.img_list[i].angle = -30 if self.img_list[i].vector_x > 0 else 30

        self.enabled = True

    def draw(self, scene, deltatime):
        if not self.enabled:
            return
        for pict in self.img_list:
            rotated_image = pygame.transform.rotate(pict.img, -pict.angle)
            pict.rect = rotated_image.get_rect(center=pict.img.get_rect(topleft=(pict.x, pict.y)).center)
            scene.blit(rotated_image, pict.rect)

            # scene.blit(pict.img, (pict.x, pict.y))

    def act(self, deltatime):
        if not self.enabled:
            return

        for pict in self.img_list:

            if abs(pict.vector_x) > 0.1:
                pict.vector_x *= 0.999999
                if pict.angle > 0:
                    pict.angle += pict.vector_x * deltatime
                else:
                    pict.angle -= -pict.vector_x * deltatime

            pict.vector_y += SnowFlake.HEIGHT * 0.65 * deltatime

            pict.x += pict.vector_x * deltatime
            pict.y += pict.vector_y * deltatime

            if pict.y + pict.img.get_height() > SnowFlake.HEIGHT:
                pict.vector_y *= -0.5
                pict.y += pict.vector_y * deltatime

        if self.img_list[9].y > SnowFlake.HEIGHT - pict.img.get_height() and abs(self.img_list[9].vector_y) < 250:
            self.enabled = False
