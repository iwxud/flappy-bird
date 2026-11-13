# -*- coding: utf-8 -*-
"""Точка входа. Запуск:  python main.py"""
import os
import sys

# чтобы модули src.* находились при запуске из любой директории
BASE = os.path.dirname(os.path.abspath(__file__))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from src.game import main  # noqa: E402

if __name__ == "__main__":
    main()
