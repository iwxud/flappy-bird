# -*- coding: utf-8 -*-
"""Юнит-тесты логики Flappy Bird. Запуск: python tests/test_game.py или pytest."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame  # noqa: E402
from src import config  # noqa: E402
from src.bird import Bird  # noqa: E402
from src.pipes import PipePair, PipeManager  # noqa: E402
from src.score import Score  # noqa: E402


def make_bird():
    frames = [pygame.Surface(config.BIRD_SIZE, pygame.SRCALPHA) for _ in range(3)]
    return Bird(frames)


class TestBird(unittest.TestCase):
    def test_gravity_pulls_down(self):
        b = make_bird()
        y0 = b.y
        for _ in range(30):
            b.update()
        self.assertGreater(b.y, y0)

    def test_flap_goes_up(self):
        b = make_bird()
        for _ in range(10):
            b.update()
        b.flap()
        self.assertEqual(b.vel_y, config.FLAP_STRENGTH)
        y0 = b.y
        b.update()
        self.assertLess(b.y, y0)

    def test_max_fall_speed(self):
        b = make_bird()
        b.vel_y = 100
        b.update()
        self.assertLessEqual(b.vel_y, config.MAX_FALL_SPEED)

    def test_hitbox_smaller_than_sprite(self):
        b = make_bird()
        hb = b.hit_mask()
        r = b.rect
        self.assertLess(hb.width, r.width)
        self.assertLess(hb.height, r.height)


class TestPipes(unittest.TestCase):
    def test_gap_is_consistent(self):
        p = PipePair(500)
        self.assertEqual(p.bottom_rect.y - p.top_rect.bottom, config.PIPE_GAP)

    def test_move_left(self):
        p = PipePair(500)
        x0 = p.top_rect.x
        p.move(config.PIPE_SPEED, dt_scale=1.0)
        self.assertLess(p.top_rect.x, x0)

    def test_collision_detects_overlap(self):
        p = PipePair(200)
        hit = p.top_rect.inflate(-10, -10)  # точка внутри верхней трубы
        self.assertTrue(p.collides(hit))
        gap_point = pygame.Rect(p.x + 10, p.gap_center - 5, 10, 10)
        self.assertFalse(p.collides(gap_point))

    def test_scoring_once_per_pipe(self):
        pm = PipeManager()
        pipe = PipePair(200)
        pm.pipes.append(pipe)
        pipe.move(200, 1.0)  # уводим влево за птицу
        gained1 = pm.update(0, 1.0, config.BIRD_X)
        gained2 = pm.update(0, 1.0, config.BIRD_X)
        self.assertEqual(gained1, 1)
        self.assertEqual(gained2, 0)


class TestScore(unittest.TestCase):
    def test_add_and_medals(self):
        s = Score()
        s.current = 0
        s.add(config.MEDAL_BRONZE)
        self.assertEqual(s.medal(), "BRONZE")
        s.add(config.MEDAL_SILVER - config.MEDAL_BRONZE)
        self.assertEqual(s.medal(), "SILVER")
        s.add(config.MEDAL_GOLD - config.MEDAL_SILVER)
        self.assertEqual(s.medal(), "GOLD")

    def test_new_best_detection(self):
        s = Score()
        s.best = 5
        s.current = 6
        self.assertTrue(s.is_new_best())


class TestGameIntegration(unittest.TestCase):
    """Прогон игры headless на несколько сотен кадров."""

    def test_runs_without_crash(self):
        from src.game import Game, GameState
        game = Game(headless=True)
        # старт из меню
        game._start_game()
        self.assertEqual(game.state, GameState.PLAYING)
        # крутим 300 «кадров» с автопилотом: прыгаем, когда ниже центра зазора
        for i in range(300):
            if game.state == GameState.PLAYING and game.bird.alive:
                if game.bird.vel_y > 2:
                    game.bird.flap()
            game.update(1000 / config.FPS)
            game.on_frame_end()
            game.draw()
        self.assertIn(game.state, (GameState.PLAYING, GameState.GAME_OVER))
        pygame.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)
