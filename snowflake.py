from random import randint

import pygame


class SnowFlake:
    HEIGHT = None
    WIDTH = None

    SNOW = pygame.image.load("images/snow.png")

    image_files = ["images/snowflake01.png",
                   "images/snowflake02.png",
                   "images/snowflake03.png",
                   "images/snowflake04.png",
                   "images/snowflake05.png",
                   "images/snowflake06.png",
                   "images/snowflake07.png",
                   "images/snowflake08.png",
                   "images/snowflake09.png"]
    wind = None

    def __init__(self):
        self.x = randint(-SnowFlake.WIDTH, SnowFlake.WIDTH * 2)
        self.y = randint(-SnowFlake.HEIGHT, -50)

        self.angle = 2

        self.image = pygame.image.load(SnowFlake.image_files[randint(0, len(SnowFlake.image_files) - 1)])
        scale = SnowFlake.HEIGHT / SnowFlake.WIDTH
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale,
                                                         self.image.get_height() * scale))

        self.accel_y = randint(int(SnowFlake.HEIGHT // 400 * self.image.get_height()),
                               int(SnowFlake.HEIGHT // 200 * self.image.get_height()))

        self.width_rotate = self.image.get_width() // 2
        self.height_rotate = self.image.get_height() // 2
        self.change_angle = randint(3, 48)

        self.enable = True

    def act(self, deltatime):
        if self.y > SnowFlake.HEIGHT:
            return

        self.x += SnowFlake.wind * deltatime
        self.y += self.accel_y * deltatime

        if (self.x < 0 - self.width_rotate and SnowFlake.wind < 0 or
            self.x > SnowFlake.WIDTH) and SnowFlake.wind > 0:
            self.enable = False

        self.angle += self.change_angle * deltatime
        if self.angle > 360:
            self.angle = 0

        if self.y > SnowFlake.HEIGHT:
            return True

    def draw(self, scene):
        if self.y > SnowFlake.HEIGHT:
            return

        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)
        scene.blit(rotated_image, new_rect)

    @staticmethod
    def wind_of_change(deltatime, pos):
        scroll = ((SnowFlake.WIDTH // 2 - pos.x) * -1)
        SnowFlake.wind += scroll * deltatime
        if SnowFlake.wind < -300:
            SnowFlake.wind = -300
        elif SnowFlake.wind > 300:
            SnowFlake.wind = 300
