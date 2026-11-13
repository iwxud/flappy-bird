# Flappy Bird (Python + Pygame)

Классическая Flappy Bird на Python. Игра запускается **сразу**, даже без спрайтов —
пока ты не положишь свои картинки в `assets/`, вместо них рисуются цветные заглушки.

## Структура проекта

```
flappy_bird/
├── main.py                  # запуск игры
├── requirements.txt         # зависимости
├── highscore.txt            # рекорд (создаётся автоматически)
├── assets/
│   ├── sprites/
│   │   ├── background/      # day_background.png, ground.png
│   │   ├── bird/            # yellowbird-upflap/midflap/downflap.png
│   │   ├── pipes/           # green_pipe.png
│   │   └── ui/              # scoreboard.png, button_play.png, text_gameover.png
│   ├── fonts/               # любые .ttf/.otf — подхватятся автоматически
│   └── sounds/              # wing.ogg, score.ogg, hit.ogg, die.ogg
├── src/
│   ├── config.py            # ВСЕ настройки игры (физика, трубы, цвета...)
│   ├── game.py              # главный цикл и состояния
│   ├── bird.py              # птица: гравитация, прыжок, анимация
│   ├── pipes.py             # трубы: спавн, движение, очки, коллизии
│   ├── ground.py            # прокрутка земли
│   ├── score.py             # счёт и рекорд
│   ├── ui.py                # меню, счёт, экран Game Over
│   ├── assets_loader.py     # загрузка ассетов + заглушки
│   └── sprites_drawing.py   # рисование заглушек (когда спрайтов нет)
└── tests/                   # автотесты
```

## Установка и запуск

```bash
pip install -r requirements.txt
python main.py
```

## Управление

| Клавиша / действие | Что делает            |
|--------------------|-----------------------|
| ПРОБЕЛ / ↑ / W / клик мыши | Взлететь (а также старт/рестарт) |
| ESC                | Пауза-выход в меню / закрыть игру |

## Как добавить свои спрайты

Смотри подробную инструкцию в [assets/README.md](assets/README.md).
Достаточно положить файлы с правильными именами — код менять не нужно.

## Настройка сложности

Всё в `src/config.py`:

- `GRAVITY` — сила притяжения (больше = быстрее падает)
- `FLAP_STRENGTH` — мощность прыжка (по модулю)
- `PIPE_GAP` — зазор между трубами (меньше = сложнее)
- `PIPE_SPEED` — скорость движения труб
- `PIPE_SPAWN_INTERVAL_MS` — частота появления труб

## Тесты

```bash
python -m pytest tests/ -v
# или без pytest:
python tests/test_game.py
```
