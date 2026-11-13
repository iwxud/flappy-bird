# -*- coding: utf-8 -*-
"""
Рисование заглушек (fallback-спрайтов) простыми фигурами pygame.
Используются, только если соответствующие PNG-файлы НЕ положены в assets/.
Как только добавишь настоящие спрайты — эти функции перестанут вызываться.
"""
import math
import pygame

from src import config


def _w(surface):
    return surface.get_width()


def _h(surface):
    return surface.get_height()


# ---------------- Птица ----------------
def _draw_bird(surface, size, wing_angle):
    w, h = size
    cx, cy = w // 2, h // 2
    body_r = (int(w * 0.42), int(h * 0.42))
    # тело
    pygame.draw.ellipse(surface, config.COLOR_BIRD,
                        (cx - body_r[0], cy - body_r[1], body_r[0] * 2, body_r[1] * 2))
    pygame.draw.ellipse(surface, (218, 176, 0), None if False else
                        (cx - body_r[0], cy - body_r[1], body_r[0] * 2, body_r[1] * 2), 2)
    # крыло
    wx = cx - int(w * 0.12)
    wy = cy + int(h * 0.05)
    wing_len = int(w * 0.3)
    dx = int(math.cos(wing_angle) * wing_len)
    dy = int(math.sin(wing_angle) * wing_len * 0.6)
    pygame.draw.line(surface, (240, 200, 40), (wx, wy), (wx - dx, wy + dy), max(3, h // 8))
    # глаз
    ex = cx + int(w * 0.18)
    ey = cy - int(h * 0.15)
    er = max(3, h // 7)
    pygame.draw.circle(surface, config.COLOR_BIRD_EYE, (ex, ey), er)
    pygame.draw.circle(surface, (30, 30, 30), (ex + 1, ey), max(2, er // 2))
    # клюв
    bx = cx + int(w * 0.38)
    by = cy + int(h * 0.05)
    pygame.draw.polygon(surface, config.COLOR_BIRD_BEAK,
                        [(bx, by - 4), (bx + w // 6, by), (bx, by + 4)])


def fallback_bird_up(surface, size):
    _draw_bird(surface, size, wing_angle=-math.pi / 3)


def fallback_bird_mid(surface, size):
    _draw_bird(surface, size, wing_angle=0)


def fallback_bird_down(surface, size):
    _draw_bird(surface, size, wing_angle=math.pi / 4)


# ---------------- Трубы ----------------
def fallback_pipe_segment(size):
    """Вертикальная текстура трубы (повторяется по высоте)."""
    w, h = size
    surf = pygame.Surface((w, h))
    surf.fill(config.COLOR_PIPE)
    # продольные блики/тени
    pygame.draw.rect(surf, (130, 230, 100), (int(w * 0.15), 0, int(w * 0.15), h))
    pygame.draw.rect(surf, config.COLOR_PIPE_EDGE, (int(w * 0.75), 0, int(w * 0.12), h))
    surf.fill(config.COLOR_SKY, (0, 0, 0, 0)) if False else None
    return surf


def draw_pipe_pair(screen, top_rect, bottom_rect, pipe_img):
    """Рисует пару труб из одной текстуры (обрезая нужные куски)."""
    ih = pipe_img.get_height()
    # верхняя труба — «шапкой» вниз: отражаем по вертикали
    flipped = pygame.transform.flip(pipe_img, False, True)
    # сколько раз повторяем текстуру, чтобы покрыть высоту
    def fill_part(rect, img_src):
        remaining = rect.height
        y = rect.bottom - remaining  # стартуем с верха rect
        # шапка (край трубы) рисуется у края зазора
        cap_h = min(32, rect.height)
        first = True
        while remaining > 0:
            piece_h = min(ih, remaining)
            chunk = img_src.subsurface((0, ih - piece_h, pipe_img.get_width(), piece_h)) \
                if False else pygame.transform.scale(img_src, (rect.width, piece_h))
            screen.blit(chunk, (rect.x, y))
            y += piece_h
            remaining -= piece_h
            first = False
    fill_part(top_rect, flipped)
    fill_part(bottom_rect, pipe_img)
    # «манжеты» труб у зазора
    cap_w = top_rect.width + 8
    cap_h = 26
    for r, base_y in ((top_rect, top_rect.bottom - cap_h), (bottom_rect, bottom_rect.y)):
        cap = pygame.Rect(r.x - 4, base_y, cap_w, cap_h)
        pygame.draw.rect(screen, config.COLOR_PIPE, cap, border_radius=4)
        pygame.draw.rect(screen, config.COLOR_PIPE_EDGE, cap, 3, border_radius=4)


# ---------------- Фон и земля ----------------
def fallback_background(size):
    w, h = size
    surf = pygame.Surface(size)
    surf.fill(config.COLOR_SKY)
    # облака-заглушки
    cloud_color = (255, 255, 255)
    for (cx, cy, cw) in ((60, 90, 50), (200, 140, 70), (320, 70, 45), (140, 220, 60)):
        pygame.draw.ellipse(surf, cloud_color, (cx, cy, cw, cw // 2))
    # кусты над землёй
    bush_y = h - config.GROUND_HEIGHT - 20
    for bx in range(-20, w + 40, 60):
        pygame.draw.circle(surf, (80, 180, 80), (bx, bush_y + 20), 30)
    return surf


def fallback_ground(size):
    w, h = size
    surf = pygame.Surface(size)
    surf.fill(config.COLOR_GROUND)
    # полосатая кромка сверху
    stripe_h = 12
    pygame.draw.rect(surf, (120, 200, 80), (0, 0, w, stripe_h))
    for x in range(0, w, 24):
        pygame.draw.polygon(surf, config.COLOR_GROUND_LINE,
                            [(x, stripe_h), (x + 12, stripe_h), (x + 6, stripe_h + 8)])
    pygame.draw.line(surf, config.COLOR_GROUND_LINE, (0, stripe_h + 10), (w, stripe_h + 10), 2)
    # «крапинки»
    for x in range(8, w, 40):
        pygame.draw.rect(surf, (200, 160, 110), (x, stripe_h + 25, 16, 6))
    return surf


# ---------------- UI ----------------
def fallback_scoreboard(surface, size):
    w, h = size
    panel = pygame.Rect(0, 0, w, h)
    pygame.draw.rect(surface, (222, 184, 120), panel, border_radius=12)
    pygame.draw.rect(surface, (160, 120, 60), panel, 4, border_radius=12)


def fallback_button_play(surface, size):
    w, h = size
    btn = pygame.Rect(0, 0, w, h)
    pygame.draw.rect(surface, (250, 200, 60), btn, border_radius=14)
    pygame.draw.rect(surface, (180, 130, 20), btn, 4, border_radius=14)
    # треугольник «play»
    pygame.draw.polygon(surface, (255, 255, 255),
                        [(w * 0.38, h * 0.3), (w * 0.38, h * 0.7), (w * 0.68, h * 0.5)])


def fallback_gameover_text(surface, size):
    w, h = size
    font = pygame.font.Font(None, int(h * 0.7))
    txt = font.render("GAME OVER", True, (255, 255, 255))
    shadow = font.render("GAME OVER", True, (120, 60, 0))
    surface.blit(shadow, (w // 2 - shadow.get_width() // 2 + 2, h // 2 - shadow.get_height() // 2 + 2))
    surface.blit(txt, (w // 2 - txt.get_width() // 2, h // 2 - txt.get_height() // 2))
