# -*- coding: utf-8 -*-
"""
Все настройки игры в одном месте.
Меняй значения здесь — код трогать не нужно.
"""
import os

# ---------- Пути ----------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # flappy_bird/
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites")
BG_DIR = os.path.join(SPRITES_DIR, "background")
BIRD_DIR = os.path.join(SPRITES_DIR, "bird")
PIPES_DIR = os.path.join(SPRITES_DIR, "pipes")
UI_DIR = os.path.join(SPRITES_DIR, "ui")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")

# ---------- Экран ----------
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Flappy Bird"

# ---------- Физика птицы ----------
GRAVITY = 0.45          # px/кадр^2 вниз
FLAP_STRENGTH = -8.0    # импульс при нажатии (вверх)
MAX_FALL_SPEED = 12.0   # предельная скорость падения
BIRD_X = 80             # фиксированная позиция птицы по X
BIRD_SIZE = (44, 32)    # размер спрайта, если fallback-фигура

# ---------- Трубы ----------
PIPE_WIDTH = 70
PIPE_GAP = 160          # зазор между верхней и нижней трубой
PIPE_SPEED = 3.0        # px/кадр
PIPE_SPAWN_INTERVAL_MS = 1500  # как часто появляются новые трубы
PIPE_MARGIN_TOP = 60    # минимальный отступ верха верхней трубы от края экрана

# ---------- Земля ----------
GROUND_HEIGHT = 100
GROUND_SCROLL_FACTOR = 1.0  # скорость земли = PIPE_SPEED * factor

# ---------- Счёт ----------
SCORE_PER_PIPE = 1
MEDAL_BRONZE = 10
MEDAL_SILVER = 20
MEDAL_GOLD = 30

# ---------- Звук ----------
SOUND_ENABLED = True
MASTER_VOLUME = 0.5

# ---------- Цвета (используются только для заглушек, если спрайтов нет) ----------
COLOR_SKY = (112, 197, 207)
COLOR_GROUND = (222, 184, 135)
COLOR_GROUND_LINE = (160, 120, 80)
COLOR_PIPE = (94, 201, 72)
COLOR_PIPE_EDGE = (60, 140, 45)
COLOR_BIRD = (255, 214, 10)
COLOR_BIRD_BEAK = (255, 120, 0)
COLOR_BIRD_EYE = (255, 255, 255)
COLOR_TEXT = (255, 255, 255)
COLOR_TEXT_SHADOW = (60, 60, 60)
