import pygame.mixer_music


"""
    Класс для хранения и воспроизведения звуков в игре.
"""
class Sounds:

    def __init__(self):
        self.explose = pygame.mixer.Sound("sounds/explode.ogg")
        self.gift = pygame.mixer.Sound("sounds/gift.ogg")

    """Хлопок снежинки"""
    def play_expl(self):
        self.explose.play()

    """Хлопок подарка"""
    def play_gift(self):
        self.gift.play()
