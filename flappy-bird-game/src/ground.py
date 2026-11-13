# -*- coding: utf-8 -*-
"""Земля, прокручивающаяся влево (бесшовный скролл двух копий)."""
import pygame

from src import config


class Ground:
    def __init__(self, texture):
        self.texture = texture
        self.tw = texture.get_width()
        self.x1 = 0.0
        self.y = config.SCREEN_HEIGHT - config.GROUND_HEIGHT

    def update(self, speed, dt_scale=1.0):
        self.x1 -= speed * config.GROUND_SCROLL_FACTOR * dt_scale
        # бесшовность: держим offset в пределах одной текстуры
        if self.x1 <= -self.tw:
            self.x1 += self.tw

    def draw(self, screen):
        ix = int(round(self.x1))
        screen.blit(self.texture, (ix, self.y))
        screen.blit(self.texture, (ix + self.tw, self.y))
        screen.blit(self.texture, (ix - self.tw, self.y))

    def top_y(self):
        return self.y
