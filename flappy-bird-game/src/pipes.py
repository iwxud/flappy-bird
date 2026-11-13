# -*- coding: utf-8 -*-
"""Трубы: появление, движение, подсчёт очков и столкновения."""
import random
import pygame

from src import config
from src.sprites_drawing import draw_pipe_pair


class PipePair:
    def __init__(self, x):
        self.x = float(x)
        self.width = config.PIPE_WIDTH
        playable_h = config.SCREEN_HEIGHT - config.GROUND_HEIGHT
        min_center = config.PIPE_MARGIN_TOP + config.PIPE_GAP // 2
        max_center = playable_h - config.PIPE_MARGIN_TOP - config.PIPE_GAP // 2
        self.gap_center = random.randint(min_center, max_center)
        self.scored = False

        gap_half = config.PIPE_GAP // 2
        self.top_rect = pygame.Rect(int(self.x), 0, self.width,
                                    self.gap_center - gap_half)
        self.bottom_rect = pygame.Rect(int(self.x), self.gap_center + gap_half,
                                       self.width,
                                       playable_h - (self.gap_center + gap_half))

    def move(self, speed, dt_scale=1.0):
        self.x -= speed * dt_scale
        dx = int(round(self.x)) - self.top_rect.x
        self.top_rect.x += dx
        self.bottom_rect.x += dx

    def offscreen(self):
        return self.top_rect.right < -10

    def collides(self, hitbox):
        return hitbox.colliderect(self.top_rect) or hitbox.colliderect(self.bottom_rect)

    def passed(self, bird_x):
        return not self.scored and self.top_rect.right < bird_x

    def draw(self, screen, pipe_img, use_fallback_caps):
        draw_pipe_pair(screen, self.top_rect, self.bottom_rect, pipe_img)


class PipeManager:
    def __init__(self):
        self.pipes = []
        self.spawn_timer_ms = 0

    def reset(self):
        self.pipes.clear()
        self.spawn_timer_ms = config.PIPE_SPAWN_INTERVAL_MS  # первая труба не сразу

    def update(self, delta_ms, dt_scale, bird_x):
        """Возвращает количество заработанных очков на этом кадре."""
        self.spawn_timer_ms += delta_ms
        if self.spawn_timer_ms >= config.PIPE_SPAWN_INTERVAL_MS:
            self.spawn_timer_ms = 0
            self.pipes.append(PipePair(config.SCREEN_WIDTH + 10))

        for p in self.pipes:
            p.move(config.PIPE_SPEED, dt_scale)

        self.pipes = [p for p in self.pipes if not p.offscreen()]

        gained = 0
        for p in self.pipes:
            if p.passed(bird_x):
                p.scored = True
                gained += config.SCORE_PER_PIPE
        return gained

    def any_collision(self, hitbox):
        return any(p.collides(hitbox) for p in self.pipes)

    def draw(self, screen, pipe_img, fallback_caps):
        for p in self.pipes:
            p.draw(screen, pipe_img, fallback_caps)
