# Если отсутствуют библиотеки, выполнить следующие команды
# в терминале Windows (или в виртуальном окружении)
# pip install pygame
# pip install pywin32
# pip install pyautogui

import ctypes

import pyautogui
import pygame
import win32api
import win32con
import win32gui

from snowdrift import SnowDrift
from snowexplose import SnowExplose
from snowflake import SnowFlake
from random import randint
from ctypes import wintypes

from sounds import Sounds

pygame.init()
scene = pygame.display.set_mode((0, 0),
                                pygame.NOFRAME,
                                pygame.FULLSCREEN)
pygame.display.set_caption("Snow Desktop")

SnowFlake.WIDTH = pygame.display.Info().current_w
SnowFlake.HEIGHT = pygame.display.Info().current_h

clock = pygame.time.Clock()

# Зелёный хромакей
transparency = (0, 0, 0)

# =============================
# Прозрачное окно на весь экран и на передний план
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*transparency), 0, win32con.LWA_COLORKEY)
user32 = ctypes.WinDLL("user32")
user32.SetWindowPos.restype = wintypes.HWND
user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND,
                                wintypes.INT, wintypes.INT,
                                wintypes.INT, wintypes.INT, wintypes.UINT]
user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001)
# =============================
playgame = True
FPS = 60                    # Изменить, чтобы увеличить/уменьшить ФПС
deltatime = 0               # Синхронизация движения с частотой кадров
flakes_list = []            # Снежинки
snow_exploses_list = []      # Эффекты при клике на снежинку
max_count_flakes = 800      # Уменьшить, если тормозит
frame = 0
# =============================

SnowFlake.wind = randint(int(-SnowFlake.WIDTH * 0.05), int(SnowFlake.WIDTH * 0.05))
snowdrift = SnowDrift()

sounds = Sounds()

# snow_exploses_list.append(SnowExplose(SnowFlake.WIDTH // 2, SnowFlake.HEIGHT // 2, sounds))

for i in range(int(max_count_flakes * 0.75)):
    flakes_list.append(SnowFlake())

while playgame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playgame = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                playgame = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for flake in flakes_list:
                if flake.rect.collidepoint(x, y):
                    snow_exploses_list.append(SnowExplose(x, y, sounds))
                    flakes_list.remove(flake)
                    flakes_list.append(SnowFlake())
                    break


    scene.fill(transparency)

    # Отрисовка снежинок и перемещение
    for flake in flakes_list:
        flake.draw(scene)
        flake.act(deltatime)

    for snow_exploses in snow_exploses_list:
        snow_exploses.draw(scene)

        # Удаляем из списка, когда вышла за нижнюю границу экрана
        if flake.y > SnowFlake.HEIGHT:
            flakes_list.remove(flake)
            if len(flakes_list) < max_count_flakes:
                flakes_list.append(SnowFlake())

    # Отрисовка "сугробов"
    snowdrift.draw(scene)

    # Движение сугроба вверх каждый пятый кадр
    if frame % 5 == 0:
        snowdrift.up(deltatime)

    pygame.display.update()

    for snow_exploses in snow_exploses_list:
        snow_exploses.act(deltatime)
        if not snow_exploses.enabled:
            snow_exploses_list.remove(snow_exploses)

    # Контроль позиции курсора мыши и изменение ветра
    if frame % 5 == 0:
        SnowFlake.wind_of_change(deltatime, pyautogui.position())

    deltatime = clock.tick(FPS) / 1000
    frame += 1
