# -*- coding: utf-8 -*-
"""Экраны и отрисовка UI: меню, игра, game over."""
import pygame

from src import config


class UI:
    def __init__(self, assets):
        self.assets = assets
        self.font_big = assets.get_font(48)
        self.font_mid = assets.get_font(28)
        self.font_small = assets.get_font(20)

        self.title_img = self.font_big.render("Flappy Bird", True, config.COLOR_TEXT)
        self.title_shadow = self.font_big.render("Flappy Bird", True, config.COLOR_TEXT_SHADOW)
        self.hint_img = self.font_small.render("Нажми ПРОБЕЛ или клик, чтобы взлететь",
                                               True, config.COLOR_TEXT)
        self.gameover_img = assets.ui_gameover_text()
        self.scoreboard = assets.ui_scoreboard()
        self.button_play = assets.ui_button_play()

        # масштабированные кнопки/панели под экран
        self.play_btn_rect = pygame.Rect(0, 0, 90, 90)
        self.scoreboard_rect = pygame.Rect(0, 0, 300, 170)

    # ---------------- helpers ----------------
    @staticmethod
    def _blit_center(screen, img, cx, cy):
        screen.blit(img, img.get_rect(center=(cx, cy)))

    def _text_with_shadow(self, screen, text, font, cx, cy,
                          color=config.COLOR_TEXT, shadow=config.COLOR_TEXT_SHADOW):
        img = font.render(text, True, color)
        sh = font.render(text, True, shadow)
        r = img.get_rect(center=(cx, cy))
        screen.blit(sh, (r.x + 2, r.y + 2))
        screen.blit(img, r)
        return r

    # ---------------- Меню ----------------
    def draw_menu(self, screen, bird, t):
        w, h = config.SCREEN_WIDTH, config.SCREEN_HEIGHT
        self._blit_center(screen, self.title_shadow, w // 2 + 3, h // 5 + 3)
        self._blit_center(screen, self.title_img, w // 2, h // 5)

        # птица «парит» на месте (синусоида)
        import math
        by = h // 2 + int(12 * math.sin(t / 18.0))
        sprite = bird.get_sprite()
        self._blit_center(screen, sprite, w // 2, by)

        self._blit_center(screen, self.hint_img, w // 2, h * 0.72)

        # кнопка play
        btn = pygame.transform.scale(self.button_play, (90, 90))
        self.play_btn_rect = btn.get_rect(center=(w // 2, h * 0.86))
        screen.blit(btn, self.play_btn_rect)

    # ---------------- Игра ----------------
    def draw_score(self, screen, score_value):
        self._text_with_shadow(screen, str(score_value), self.font_big,
                               config.SCREEN_WIDTH // 2, 60)

    # ---------------- Game Over ----------------
    def draw_game_over(self, screen, score_obj):
        w, h = config.SCREEN_WIDTH, config.SCREEN_HEIGHT
        # затемнение
        veil = pygame.Surface((w, h), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 110))
        screen.blit(veil, (0, 0))

        go = pygame.transform.scale(self.gameover_img, (220, 55))
        self._blit_center(screen, go, w // 2, h * 0.25)

        panel = pygame.transform.scale(self.scoreboard, (300, 170))
        pr = panel.get_rect(center=(w // 2, h * 0.47))
        screen.blit(panel, pr)

        self._text_with_shadow(screen, "SCORE", self.font_small, w // 2 - 70, pr.y + 30,
                               color=(120, 70, 20), shadow=(255, 255, 255))
        self._text_with_shadow(screen, str(score_obj.current), self.font_mid,
                               w // 2 + 70, pr.y + 32,
                               color=(120, 70, 20), shadow=(255, 255, 255))
        self._text_with_shadow(screen, "BEST", self.font_small, w // 2 - 70, pr.y + 90,
                               color=(120, 70, 20), shadow=(255, 255, 255))
        self._text_with_shadow(screen, str(score_obj.best), self.font_mid,
                               w // 2 + 70, pr.y + 92,
                               color=(120, 70, 20), shadow=(255, 255, 255))

        medal = score_obj.medal()
        if medal:
            self._text_with_shadow(screen, f"MEDAL: {medal}", self.font_small,
                                   w // 2, pr.bottom - 25,
                                   color=(120, 70, 20), shadow=(255, 255, 255))

        btn = pygame.transform.scale(self.button_play, (90, 90))
        self.play_btn_rect = btn.get_rect(center=(w // 2, h * 0.78))
        screen.blit(btn, self.play_btn_rect)

        self._text_with_shadow(screen, "ПРОБЕЛ — заново, ESC — меню", self.font_small,
                               w // 2, h * 0.92)

    def play_button_clicked(self, pos):
        return self.play_btn_rect.collidepoint(pos)
