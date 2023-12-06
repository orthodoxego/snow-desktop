import pygame.mixer_music


class Sounds:

    def __init__(self):
        self.explose = pygame.mixer.Sound("sounds/explode.ogg")

    def play_expl(self):
        self.explose.play()
