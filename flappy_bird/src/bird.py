# -*- coding: utf-8 -*-
"""Птица: физика падения, прыжок, анимация и наклон."""
import math
import pygame

from src import config


class Bird:
    ANGLE_UP = -25
    ANGLE_DOWN_MAX = 75

    def __init__(self, frames):
        self.frames = frames          # список Surface (3 кадра)
        self.base_size = frames[0].get_size()
        self.x = config.BIRD_X
        self.reset()

    def reset(self):
        self.y = (config.SCREEN_HEIGHT - config.GROUND_HEIGHT) / 2
        self.vel_y = 0.0
        self.angle = 0.0
        self.anim_index = 0
        self.anim_timer = 0
        self.alive = True

    @property
    def rect(self):
        w, h = self.base_size
        return pygame.Rect(int(self.x - w / 2), int(self.y - h / 2), w, h)

    def flap(self):
        self.vel_y = config.FLAP_STRENGTH
        self.anim_index = 0   # взмах крыльев
        self.anim_timer = 0

    def update(self, dt_scale=1.0):
        if not self.alive:
            # после столкновения падаем без управления
            self.vel_y = min(self.vel_y + config.GRAVITY * dt_scale, config.MAX_FALL_SPEED)
            self.y += self.vel_y * dt_scale
            ground_y = config.SCREEN_HEIGHT - config.GROUND_HEIGHT
            if self.y > ground_y - self.base_size[1] / 2:
                self.y = ground_y - self.base_size[1] / 2
            self._update_angle()
            return
        self.vel_y = min(self.vel_y + config.GRAVITY * dt_scale, config.MAX_FALL_SPEED)
        self.y += self.vel_y * dt_scale
        self._update_angle()
        self._animate(dt_scale)

    def _update_angle(self):
        target = self.ANGLE_UP if self.vel_y < 0 else \
            min(self.ANGLE_DOWN_MAX, self.vel_y * 7)
        self.angle += (target - self.angle) * 0.15

    def _animate(self, dt_scale=1.0):
        self.anim_timer += dt_scale
        if self.anim_timer >= 8:
            self.anim_timer = 0
            self.anim_index = (self.anim_index + 1) % len(self.frames)

    def get_sprite(self):
        frame = self.frames[self.anim_index % len(self.frames)]
        if abs(self.angle) < 1:
            return frame
        return pygame.transform.rotate(frame, self.angle)

    def draw(self, screen):
        sprite = self.get_sprite()
        rect = sprite.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(sprite, rect)

    def hit_mask(self):
        """Приблизительный хитбокс чуть меньше спрайта — так играть приятнее."""
        w, h = self.base_size
        shrink_x, shrink_y = int(w * 0.15), int(h * 0.15)
        r = self.rect
        return pygame.Rect(r.x + shrink_x, r.y + shrink_y,
                           r.width - 2 * shrink_x, r.height - 2 * shrink_y)
