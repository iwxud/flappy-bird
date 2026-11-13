# -*- coding: utf-8 -*-
"""
Загрузчик ассетов.

Логика: если файл спрайта существует — загружается он,
если нет — генерируется цветная заглушка, чтобы игра работала сразу.
Так ты сможешь просто положить свои PNG/WAV в папки assets/, и всё подхватится.

Ожидаемые имена файлов (см. также assets/README.md):
  sprites/bird/yellowbird-upflap.png, yellowbird-midflap.png, yellowbird-downflap.png
  sprites/pipes/green_pipe.png            (одна текстура трубы целиком)
  sprites/background/day_background.png
  sprites/ui/scoreboard.png, sprites/ui/button_play.png, sprites/ui/text_gameover.png
  sounds/wing.ogg, sounds/score.ogg, sounds/hit.ogg, sounds/die.ogg, sounds/sfx_die.ogg
"""
import os
import pygame

from src import config


class AssetsLoader:
    def __init__(self, screen_size=(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)):
        self.screen_size = screen_size
        self._image_cache = {}
        self._sound_cache = {}
        self.missing = []  # список отсутствующих файлов (для информации)

    # ---------------- Изображения ----------------
    def load_image(self, path, size=None, colorkey=None):
        """Загружает PNG с альфа-каналом. Если файла нет — возвращает None."""
        key = (path, size, colorkey)
        if key in self._image_cache:
            return self._image_cache[key]

        image = None
        full_path = path if os.path.isabs(path) else os.path.join(config.BASE_DIR, path)
        if os.path.exists(full_path):
            try:
                image = pygame.image.load(full_path).convert_alpha()
                if colorkey is not None:
                    mask = pygame.mask.from_surface(image)
                    image = image.convert_alpha()
                    image.set_colorkey(colorkey) if False else None
                if size:
                    image = pygame.transform.scale(image, size)
            except Exception as e:
                print(f"[assets] Не удалось загрузить {full_path}: {e}")
                image = None
        else:
            self.missing.append(full_path)
        self._image_cache[key] = image
        return image

    def get_image_or_fallback(self, path, size, draw_fn):
        """Возвращает спрайт из файла либо рисует заглушку через draw_fn(surface, size)."""
        img = self.load_image(path, size=size)
        if img is not None:
            return img
        surf = pygame.Surface(size, pygame.SRCALPHA)
        draw_fn(surf, size)
        return surf

    # ---------------- Звуки ----------------
    def load_sound(self, path):
        full_path = path if os.path.isabs(path) else os.path.join(config.BASE_DIR, path)
        if full_path in self._sound_cache:
            return self._sound_cache[full_path]
        sound = None
        if os.path.exists(full_path):
            try:
                sound = pygame.mixer.Sound(full_path)
                sound.set_volume(config.MASTER_VOLUME)
            except Exception as e:
                print(f"[assets] Не удалось загрузить звук {full_path}: {e}")
                sound = None
        else:
            self.missing.append(full_path)
        self._sound_cache[full_path] = sound
        return sound

    def play(self, name):
        if not config.SOUND_ENABLED:
            return
        sound = self._sound_cache.get(name) or self.load_sound(name)
        if sound:
            sound.play()

    # ---------------- Шрифты ----------------
    def get_font(self, size, font_file=None):
        """Берёт TTF из assets/fonts, иначе системный шрифт."""
        candidates = []
        if font_file:
            candidates.append(os.path.join(config.FONTS_DIR, font_file))
        # любые ttf из папки fonts
        if os.path.isdir(config.FONTS_DIR):
            for f in sorted(os.listdir(config.FONTS_DIR)):
                if f.lower().endswith((".ttf", ".otf")):
                    candidates.append(os.path.join(config.FONTS_DIR, f))
        for c in candidates:
            if os.path.exists(c):
                try:
                    return pygame.font.Font(c, size)
                except Exception:
                    continue
        return pygame.font.Font(None, size)

    # ---------------- Готовые ресурсы ----------------
    def bird_frames(self):
        """3 кадра анимации крыльев (up/mid/down)."""
        from src.sprites_drawing import (fallback_bird_up, fallback_bird_mid,
                                          fallback_bird_down)
        names = [
            ("yellowbird-upflap.png", fallback_bird_up),
            ("yellowbird-midflap.png", fallback_bird_mid),
            ("yellowbird-downflap.png", fallback_bird_down),
        ]
        frames = []
        for fname, fb in names:
            path = os.path.join("assets", "sprites", "bird", fname)
            frames.append(self.get_image_or_fallback(path, config.BIRD_SIZE, fb))
        return frames

    def pipe_surface(self):
        path = os.path.join("assets", "sprites", "pipes", "green_pipe.png")
        target_w = config.PIPE_WIDTH
        # Стандартный спрайт трубы из оригинала: 70x272? масштабируем под наш размер
        target_h = max(config.SCREEN_HEIGHT, 400)
        img = self.load_image(path)
        if img is not None:
            w, h = img.get_size()
            scale = target_w / w
            return pygame.transform.scale(img, (target_w, int(h * scale)))
        from src.sprites_drawing import fallback_pipe_segment
        return fallback_pipe_segment((target_w, target_h))

    def background(self):
        path = os.path.join("assets", "sprites", "background", "day_background.png")
        img = self.load_image(path)
        if img is not None:
            return pygame.transform.scale(img, self.screen_size)
        from src.sprites_drawing import fallback_background
        return fallback_background(self.screen_size)

    def ground_texture(self):
        path = os.path.join("assets", "sprites", "background", "ground.png")
        img = self.load_image(path)
        w = config.SCREEN_WIDTH * 2
        h = config.GROUND_HEIGHT
        if img is not None:
            iw, ih = img.get_size()
            scale = h / ih
            tile = pygame.transform.scale(img, (int(iw * scale), h))
            ground = pygame.Surface((w, h), pygame.SRCALPHA)
            x = 0
            while x < w:
                ground.blit(tile, (x, 0))
                x += tile.get_width()
            return ground
        from src.sprites_drawing import fallback_ground
        return fallback_ground((w, h))

    def ui_scoreboard(self):
        path = os.path.join("assets", "sprites", "ui", "scoreboard.png")
        from src.sprites_drawing import fallback_scoreboard
        size = (300, 200)
        return self.get_image_or_fallback(path, size, fallback_scoreboard)

    def ui_button_play(self):
        path = os.path.join("assets", "sprites", "ui", "button_play.png")
        from src.sprites_drawing import fallback_button_play
        size = (100, 100)
        return self.get_image_or_fallback(path, size, fallback_button_play)

    def ui_gameover_text(self):
        path = os.path.join("assets", "sprites", "ui", "text_gameover.png")
        from src.sprites_drawing import fallback_gameover_text
        size = (200, 50)
        return self.get_image_or_fallback(path, size, fallback_gameover_text)

    # ---------------- Инициализация звуков ----------------
    def preload_sounds(self):
        if not pygame.mixer.get_init():
            return
        for name in ("wing", "score", "hit", "die"):
            fname = f"{name}.ogg"
            if not os.path.exists(os.path.join(config.SOUNDS_DIR, fname)):
                fname = f"{name}.wav"
            self.load_sound(os.path.join("assets", "sounds", fname))
