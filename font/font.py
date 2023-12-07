import pygame

from flakes.snowflake import SnowFlake

"""
    Класс для хранения и вывода текста на экран.
"""
class Font:

    def __init__(self):
        self.font = pygame.font.Font("font/chava.ttf", 24)
        self.record_to_screen = ""
        self.current_score_to_screen = ""
        self.render_record = None
        self.render_record_black = None
        self.render_current_score = None
        self.render_current_score_black = None

    """
    Формирует строки для вывода и проверяет, изменились ли они с предыдущей отрисовки.
    Если строки изменились, то вызывается перерисовка (if).
    """
    def draw(self, scene, record, score):
        rt = f"Рекорд: {record} в мин."
        st = f"Текущее: {score if score > 0 else "---"} в мин."
        if self.record_to_screen != rt:
            self.render_record = self.font.render(rt, False, (0, 255, 50))
            self.render_record_black = self.font.render(rt, False, (20, 0, 0))
        if self.current_score_to_screen != st:
            self.render_current_score = self.font.render(st, False, (128, 255, 0))
            self.render_current_score_black = self.font.render(st, False, (20, 0, 0))

        scene.blit(self.render_record_black, (SnowFlake.WIDTH - 353, 17))
        scene.blit(self.render_record, (SnowFlake.WIDTH - 350, 20))
        scene.blit(self.render_current_score_black, (SnowFlake.WIDTH - 353, 47))
        scene.blit(self.render_current_score, (SnowFlake.WIDTH - 350, 50))