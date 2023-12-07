from random import randint

import pygame


class SnowFlake:
    HEIGHT = None
    WIDTH = None

    SNOW = pygame.image.load("images/snow.png")

    image_files = [pygame.image.load("images/snowflake01.png"),
                   pygame.image.load("images/snowflake02.png"),
                   pygame.image.load("images/snowflake03.png"),
                   pygame.image.load("images/snowflake04.png"),
                   pygame.image.load("images/snowflake05.png"),
                   pygame.image.load("images/snowflake06.png"),
                   pygame.image.load("images/snowflake07.png"),
                   pygame.image.load("images/snowflake08.png"),
                   pygame.image.load("images/snowflake09.png")]
    wind = None

    def __init__(self):
        self.x = randint(-SnowFlake.WIDTH, SnowFlake.WIDTH * 2)
        self.y = randint(-SnowFlake.HEIGHT, -50)

        self.angle = randint(1, 3)

        self.image = SnowFlake.image_files[randint(0, len(SnowFlake.image_files) - 1)]
        scale = SnowFlake.HEIGHT / SnowFlake.WIDTH
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale,
                                                         self.image.get_height() * scale))
        self.rect = self.image.get_rect()

        # Вероятность низкой скорости у больших снежинок выше
        self.accel_y = randint(int(SnowFlake.HEIGHT // 5 * 1 / self.image.get_height()),
                               int(SnowFlake.HEIGHT // 2 * 3 / self.image.get_height()))

        self.width_rotate = self.image.get_width() // 2
        self.height_rotate = self.image.get_height() // 2
        self.change_angle = randint(3, 48)
        self.circle_radius = SnowFlake.WIDTH * scale // 256

    def act(self, deltatime):
        if self.y > SnowFlake.HEIGHT:
            return

        self.x += SnowFlake.wind * (1 / self.width_rotate) * deltatime
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

        # pygame.draw.circle(scene, (219, 236, 255), (self.rect.center), self.circle_radius)
        pygame.draw.circle(scene, (239, 246, 255), (self.rect.center), self.circle_radius)

        #pygame.draw.rect(scene, (255, 255, 255), (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 0)

    @staticmethod
    def wind_of_change(deltatime, pos):
        scroll = ((SnowFlake.WIDTH // 2 - pos.x) * -1)
        SnowFlake.wind += scroll * deltatime
        if SnowFlake.wind < -SnowFlake.WIDTH / 2:
            SnowFlake.wind = -SnowFlake.WIDTH / 2
        elif SnowFlake.wind > SnowFlake.WIDTH / 2:
            SnowFlake.wind = SnowFlake.WIDTH / 2
