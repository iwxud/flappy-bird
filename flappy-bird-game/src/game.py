# -*- coding: utf-8 -*-
"""Главный класс игры: состояния, цикл, ввод, столкновения."""
import sys
import pygame

from src import config
from src.assets_loader import AssetsLoader
from src.bird import Bird
from src.pipes import PipeManager
from src.ground import Ground
from src.score import Score
from src.ui import UI


class GameState:
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"


class Game:
    def __init__(self, headless=False):
        pygame.init()
        if headless:
            pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), 0)
        else:
            pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption(config.TITLE)

        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"[sound] Звук недоступен: {e}")

        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        # ассеты
        self.assets = AssetsLoader((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.bg_image = self.assets.background()
        self.pipe_img = self.assets.pipe_surface()
        self.fallback_caps = True  # шапки труб дорисовываются, если спрайт — заглушка

        # объекты
        self.bird = Bird(self.assets.bird_frames())
        self.pipes = PipeManager()
        self.ground = Ground(self.assets.ground_texture())
        self.score = Score()
        self.ui = UI(self.assets)
        self.assets.preload_sounds()

        self.state = GameState.MENU
        self.frame_count = 0
        self.death_timer = 0     # задержка перед показом game over
        self.running = True

    # ---------------- Управление ----------------
    def _start_game(self):
        self.state = GameState.PLAYING
        self.bird.reset()
        self.pipes.reset()
        self.score.reset()
        self.bird.flap()
        self.assets.play("wing")

    def _on_flap_input(self):
        if self.state == GameState.MENU:
            self._start_game()
        elif self.state == GameState.PLAYING:
            self.bird.flap()
            self.assets.play("wing")
        elif self.state == GameState.GAME_OVER:
            self._start_game()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.GAME_OVER
                        self.score.finalize()
                    elif self.state == GameState.GAME_OVER:
                        self.state = GameState.MENU
                    else:
                        self.running = False
                elif event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    self._on_flap_input()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.state != GameState.PLAYING and \
                        self.ui.play_button_clicked(event.pos):
                    self._start_game()
                else:
                    self._on_flap_input()

    # ---------------- Логика ----------------
    def _check_collisions(self):
        hitbox = self.bird.hit_mask()
        ground_y = config.SCREEN_HEIGHT - config.GROUND_HEIGHT
        if hitbox.bottom >= ground_y:
            return True
        if hitbox.top <= 0:
            # вылет за верх экрана не смертелен, как в оригинале, но ограничим
            self.bird.y = max(self.bird.y, self.bird.base_size[1] / 2 - 10)
        if self.pipes.any_collision(hitbox):
            return True
        return False

    def _die(self):
        self.bird.alive = False
        self.death_timer = 0
        self.assets.play("hit")
        self.assets.play("die")

    def update(self, dt_ms):
        dt_scale = dt_ms / (1000.0 / config.FPS)  # 1.0 при 60 FPS
        self.frame_count += 1

        if self.state == GameState.MENU:
            self.ground.update(config.PIPE_SPEED, dt_scale)
            # анимация крыльев в меню
            self.bird.anim_timer += dt_scale
            if self.bird.anim_timer >= 8:
                self.bird.anim_timer = 0
                self.bird.anim_index = (self.bird.anim_index + 1) % len(self.bird.frames)

        elif self.state == GameState.PLAYING:
            self.bird.update(dt_scale)
            gained = self.pipes.update(dt_ms, dt_scale, self.bird.x)
            if gained:
                self.score.add(gained)
                self.assets.play("score")
            self.ground.update(config.PIPE_SPEED, dt_scale)

            if self.bird.alive and self._check_collisions():
                self._die()

        elif self.state == GameState.GAME_OVER:
            self.bird.update(dt_scale)
            self.death_timer += dt_ms

    def on_frame_end(self):
        """После смерти ждём падения птицы и показываем панель."""
        if self.state == GameState.PLAYING and not self.bird.alive:
            ground_y = config.SCREEN_HEIGHT - config.GROUND_HEIGHT
            landed = self.bird.rect.bottom >= ground_y
            if landed or self.death_timer > 1200:
                self.state = GameState.GAME_OVER
                self.score.finalize()

    # ---------------- Отрисовка ----------------
    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        self.pipes.draw(self.screen, self.pipe_img, self.fallback_caps)
        self.bird.draw(self.screen)
        self.ground.draw(self.screen)

        if self.state == GameState.MENU:
            self.ui.draw_menu(self.screen, self.bird, self.frame_count)
        elif self.state == GameState.PLAYING:
            self.ui.draw_score(self.screen, self.score.current)
        elif self.state == GameState.GAME_OVER:
            self.ui.draw_game_over(self.screen, self.score)

        pygame.display.flip()

    # ---------------- Главный цикл ----------------
    def run(self):
        while self.running:
            dt = self.clock.tick(config.FPS)
            dt = min(dt, 50)  # защита от «скачков» при лагах
            self.handle_events()
            self.update(dt)
            self.on_frame_end()
            self.draw()
        pygame.quit()


def main():
    headless = "--headless" in sys.argv
    Game(headless=headless).run()


if __name__ == "__main__":
    main()
