from random import randint
from flakes.snowflake import SnowFlake
import pygame


class Gift:
    HEIGHT = None
    WIDTH = None

    image = pygame.image.load("images/others/gift.png")

    def __init__(self):
        self.x = randint(0, SnowFlake.WIDTH - 100)
        self.y = randint(-SnowFlake.HEIGHT, -100)

        self.angle = randint(1, 3)

        self.image = Gift.image
        scale = SnowFlake.HEIGHT / SnowFlake.WIDTH
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale / 2,
                                                         self.image.get_height() * scale / 2))
        self.rect = self.image.get_rect()

        # Вероятность низкой скорости у больших подарков выше
        self.accel_y = randint(int(SnowFlake.HEIGHT // 5 * 1 / self.image.get_height()),
                               int(SnowFlake.HEIGHT // 2 * 3 / self.image.get_height()))

        self.width_rotate = self.image.get_width() // 3
        self.height_rotate = self.image.get_height() // 3
        self.change_angle = randint(5, 10)

    def act(self, deltatime):
        if self.y > SnowFlake.HEIGHT:
            return

        self.x += SnowFlake.wind * (1 / self.width_rotate) * deltatime / 3
        self.y += self.accel_y * deltatime

        self.angle += self.change_angle * deltatime
        if self.angle > 360:
            self.angle = 0

        if self.y > SnowFlake.HEIGHT:
            return True

    def draw(self, scene):
        if self.y > SnowFlake.HEIGHT:
            return

        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        self.rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)
        scene.blit(rotated_image, self.rect)
