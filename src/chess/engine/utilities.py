from __future__ import annotations

import os
import sys

import pygame as pg


def resource_path(relative_path):
    """
    Must wrap the relative path with this function, otherwise the game
    cannot be exported into an executable file.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def load_image(name, relative_dir="chess/data/", colorkey=None, scale=1):
    """
    Must wrap the relative path of an image with this function,
    otherwise the game cannot be exported into an executable file.
    """
    # fullname = os.path.join(data_dir, name)
    fullname = resource_path(relative_dir + name)
    image = pg.image.load(fullname)
    # image = image.convert()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()


class colors:
    BLUE = "\033[94m"
    RED = "\033[91m"
    END = "\033[0m"
