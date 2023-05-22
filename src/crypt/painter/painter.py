from PIL import Image
from random import (
    randint,
    sample,
)
from math import (
    sin,
    pi,
    sqrt,
)
from itertools import product

from .exceptions import WrongImageSizeError


class Painter:
    def __init__(self, width: int = 255, height: int = 255):
        try:
            width = int(width)
            height = int(height)
        except ValueError:
            raise WrongImageSizeError

        if width <= 0 or height <= 0:
            raise WrongImageSizeError

        self.width = width
        self.height = height

        self.drawing_types = {
            "sinusoidal": self._sinusoidal_draw,
            "circular": self._circular_draw,
            "transition": self._transition_draw,
        }

    def get_random_color_component(self):
        return randint(0, 255)

    def get_random_color(self):
        return (randint(0, 255), randint(0, 255), randint(0, 255))

    def _shuffle_color_components(self, r, g, b):
        color = [r, g, b]
        color = sample(color, 3)
        return tuple(color)

    def _transition_draw(self, pixels: list):
        base_color = self.get_random_color()
        blue = self.get_random_color_component()

        for x, y in product(range(self.width), range(self.height)):
            pixels[x, y] = (
                int(base_color[0] + x / self.width * 255),
                int(base_color[1] + y / self.height * 255),
                blue,
            )
        return pixels

    def _circular_draw(self, pixels: list):
        center_x = self.width // 2
        center_y = self.height // 2
        max_distance = sqrt(center_x**2 + center_y**2)
        blue = self.get_random_color_component()

        for x, y in product(range(self.width), range(self.height)):
            distance = sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            ratio = distance / max_distance

            pixels[x, y] = (
                int((1 - ratio) * 255),
                int(ratio * 255),
                blue,
            )
        return pixels

    def _sinusoidal_draw(self, pixels: list):
        blue = self.get_random_color_component()

        for x, y in product(range(self.width), range(self.height)):
            pixels[x, y] = (
                int((sin(x / self.width * pi) + 1) * 0.5 * 255),
                int((sin(y / self.height * pi) + 1) * 0.5 * 255),
                blue,
            )
        return pixels

    def draw(self, drawing_type=None):
        img = Image.new("RGB", (self.width, self.height), "white")
        pixels = img.load()

        if drawing_type is None:
            return img

        pixels = self.drawing_types[drawing_type](pixels)

        return img
