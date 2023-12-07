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

import time

from flakes.gift import Gift
from font.font import Font
from flakes.snowdrift import SnowDrift
from flakes.snowexplose import SnowExplose
from flakes.snowflake import SnowFlake
from flakes.giftexplose import GiftExplose
from random import randint
from ctypes import wintypes

from sounds.sounds import Sounds

try:
    with open("record.dat", "r", encoding="UTF-8") as f:
        record = float(f.readline())
except FileNotFoundError:
    record = 0
except ValueError:
    record = 0

pygame.init()
scene = pygame.display.set_mode((0, 0),
                                pygame.NOFRAME,
                                pygame.FULLSCREEN)
pygame.display.set_caption("Snow Desktop")

SnowFlake.WIDTH = pygame.display.Info().current_w
SnowFlake.HEIGHT = pygame.display.Info().current_h

clock = pygame.time.Clock()

# Хромакей
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
gifts_list = []             # Подарки
snow_exploses_list = []     # Эффекты при клике на снежинку
gift_exploses_list = []     # Эффекты при клике на подарок
max_flakes = 300            # Уменьшить, если тормозит
max_gifts = 1               # Макс. количество подарков на экране
count_fire = 0              # Количество сбитых снежинок
score = 0                   # Текущие сбитые снежинки в секунду
tm = time.time()
frame = 0
font = Font()
# =============================

SnowFlake.wind = randint(int(-SnowFlake.WIDTH * 0.05), int(SnowFlake.WIDTH * 0.05))
snowdrift = SnowDrift()

sounds = Sounds()

# snow_exploses_list.append(SnowExplose(SnowFlake.WIDTH // 2, SnowFlake.HEIGHT // 2, sounds))

for i in range(max_flakes):
    flakes_list.append(SnowFlake())
for i in range(max_gifts):
    gifts_list.append(Gift())


while playgame:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playgame = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                playgame = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for gift in gifts_list:
                if gift.rect.collidepoint(x, y):
                    gift_exploses_list.append(GiftExplose(x, y, sounds))
                    gifts_list.remove(gift)

            for flake in flakes_list:
                if flake.rect.collidepoint(x, y):
                    snow_exploses_list.append(SnowExplose(x, y, sounds))
                    flakes_list.remove(flake)
                    flakes_list.append(SnowFlake())

                    count_fire += 1
                    all_time = int(time.time() - tm)
                    if all_time > 30 and count_fire > 15:
                        score = round(count_fire / (all_time / 60), 1)

                        if score > record:
                            record = score
                            with open("record.dat", "w", encoding="UTF-8") as f:
                                f.write(str(record))

                    break

    scene.fill(transparency)

    # Отрисовка снежинок и перемещение
    for flake in flakes_list:
        flake.draw(scene)
        flake.act(deltatime)

        # Удаляем из списка, когда вышла за нижнюю границу экрана
        if flake.y > SnowFlake.HEIGHT or flake.x < -SnowFlake.WIDTH // 2 or flake.x > SnowFlake.WIDTH * 1.5:
            flakes_list.remove(flake)
            if len(flakes_list) < max_flakes:
                flakes_list.append(SnowFlake())

    # Подарки-цели
    for gift in gifts_list:
        gift.draw(scene)
        gift.act(deltatime)

        if gift.y > SnowFlake.HEIGHT:
            gifts_list.remove(gift)

    # Подарки-эффекты
    for gift_exploses in gift_exploses_list:
        gift_exploses.draw(scene)

    for snow_exploses in snow_exploses_list:
        snow_exploses.draw(scene, deltatime)

    # Отрисовка "сугробов"
    snowdrift.draw(scene)

    # Движение сугроба вверх каждый пятый кадр
    if frame % 5 == 0:
        snowdrift.up(deltatime)

    # Выводить рекорды и текущую скорость если сбитых снежинок > 10
    if count_fire > 15:
        font.draw(scene, record, score)

    pygame.display.update()
    # ==========================================================================================

    for snow_exploses in snow_exploses_list:
        snow_exploses.act(deltatime)
        if not snow_exploses.enabled:
            snow_exploses_list.remove(snow_exploses)

    for gift_exploses in gift_exploses_list:
        gift_exploses.act(deltatime)
        if not gift_exploses.enabled:
            gift_exploses_list.remove(gift_exploses)

    # Контроль позиции курсора мыши и изменение ветра
    if frame % 5 == 0:
        SnowFlake.wind_of_change(deltatime, pyautogui.position())
        if frame % FPS == 0:
            if len(gifts_list) < max_gifts and randint(0, 10) < 2:
                gifts_list.append(Gift())

    deltatime = clock.tick(FPS) / 1000
    frame += 1
