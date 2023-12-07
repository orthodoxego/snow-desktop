import pygame.mixer_music


class Sounds:

    def __init__(self):
        self.explose = pygame.mixer.Sound("sounds/explode.ogg")
        self.gift = pygame.mixer.Sound("sounds/gift.ogg")

    def play_expl(self):
        self.explose.play()

    def play_gift(self):
        self.gift.play()
