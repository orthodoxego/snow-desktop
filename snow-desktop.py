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
from snowflake import SnowFlake
from random import randint
from ctypes import wintypes

pygame.init()
scene = pygame.display.set_mode((0, 0),
                                pygame.NOFRAME,
                                pygame.FULLSCREEN)

SnowFlake.WIDTH = pygame.display.Info().current_w
SnowFlake.HEIGHT = pygame.display.Info().current_h

clock = pygame.time.Clock()

transparency = (149, 208, 243)
transparency = (0, 0, 255)

hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*transparency), 0, win32con.LWA_COLORKEY)

user32 = ctypes.WinDLL("user32")
user32.SetWindowPos.restype = wintypes.HWND
user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.UINT]
user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001)

playgame = True
FPS = 60
deltatime = 0
flakes_list = []
max_count_flakes = 500
frame = 0

SnowFlake.wind = randint(int(-SnowFlake.WIDTH * 0.05), int(SnowFlake.WIDTH * 0.05))
snowdrift = SnowDrift()
for i in range(int(max_count_flakes * 0.75)):
    flakes_list.append(SnowFlake())

while playgame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playgame = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                playgame = False

    scene.fill(transparency)

    for flake in flakes_list:
        flake.draw(scene)
        flake.act(deltatime)

        if flake.y > SnowFlake.HEIGHT:
            flakes_list.remove(flake)
            if len(flakes_list) < max_count_flakes:
                flakes_list.append(SnowFlake())


    snowdrift.draw(scene)
    if frame % 5 == 0:
        snowdrift.up(deltatime)

    pygame.display.update()

    if frame % 10 == 0:
        SnowFlake.wind_of_change(deltatime, pyautogui.position())

    deltatime = clock.tick(FPS) / 1000
    frame += 1
    if frame > 1000:
        frame = 0
