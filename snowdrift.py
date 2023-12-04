import pygame.image
from snowflake import SnowFlake


class SnowDrift:

    def __init__(self):
        self.x = 0
        self.y = SnowFlake.HEIGHT + 100
        self.image = pygame.image.load("images/snowdrift.png")
        self.image = pygame.transform.scale(self.image, (SnowFlake.WIDTH, int(self.image.get_height() / (SnowFlake.WIDTH / SnowFlake.HEIGHT))))

    def draw(self, scene):
        scene.blit(self.image, (self.x, self.y))

    def up(self, deltatime):
        if self.y < SnowFlake.HEIGHT - self.image.get_height():
            return False
        self.y -= 2 * deltatime
        return True

