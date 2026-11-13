# -*- coding: utf-8 -*-
"""Счёт и рекорд (сохраняется в highscore.txt рядом с игрой)."""
import os

from src import config

HIGHSCORE_FILE = os.path.join(config.BASE_DIR, "highscore.txt")


class Score:
    def __init__(self):
        self.current = 0
        self.best = self._load_best()

    @staticmethod
    def _load_best():
        try:
            with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f:
                return int(f.read().strip() or 0)
        except Exception:
            return 0

    def add(self, n=1):
        self.current += n

    def is_new_best(self):
        return self.current > self.best

    def finalize(self):
        """Сохраняет рекорд, если побит. Возвращает True если новый рекорд."""
        if self.is_new_best():
            self.best = self.current
            try:
                with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
                    f.write(str(self.best))
            except Exception as e:
                print(f"[score] Не удалось сохранить рекорд: {e}")
            return True
        return False

    def reset(self):
        self.current = 0

    def medal(self):
        """Возвращает название медали по текущему счёту."""
        if self.current >= config.MEDAL_GOLD:
            return "GOLD"
        if self.current >= config.MEDAL_SILVER:
            return "SILVER"
        if self.current >= config.MEDAL_BRONZE:
            return "BRONZE"
        return None
