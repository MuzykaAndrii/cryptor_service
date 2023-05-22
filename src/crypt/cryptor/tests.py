from math import sqrt
from PIL import Image
from random import randint, sample
from itertools import (
    chain,
    product,
)
from typing import (
    Annotated,
    Literal,
)
from math import sin, pi, sqrt


END_OF_MESSAGE_SIGN = "/em."
END_OF_MESSAGE_SIGN_LENGTH = len(END_OF_MESSAGE_SIGN)
END_OF_MESSAGE_SIGN_LIST = list(END_OF_MESSAGE_SIGN)


class TooSmallImageError(Exception):
    pass


class InvalidBitsError(Exception):
    pass


class InvalidImageExtensionError(Exception):
    pass


class WrongImageSizeError(Exception):
    pass


class Pixel:
    def __init__(self, r, g, b):
        self.r = self._int_color_to_bin(r)
        self.g = self._int_color_to_bin(g)
        self.b = self._int_color_to_bin(b)

    def _int_color_to_bin(self, color: int) -> list[0 | 1]:
        """Decode a color component from color number to list with bits
        int -> binary -> trim leading '0b' -> add leading zeros -> cast to list with bits
        50 -> 0b110010 -> 110010 -> 00110010 -> ['0', '0', '1', '1', '0', '0', '1', '0']
        """

        color = bin(color)  # convert color number to binary
        color = color[2:]  # trim leading 0b
        color = color.zfill(8)  # fill with leading zeros
        color = list(color)  # convert str color to list

        return color

    def _bin_color_to_int(self, color: list[0 | 1]):
        return int("".join(color), 2)

    def get_color(self) -> tuple[int, int, int]:
        """Returns color in format (r, g, b)
        Example:
            self colors: [1,1,1,1,1,1,1,1], [0,0,0,0,0,0,0,0], [1,1,1,1,1,1,1,1]
            returns (255, 0, 255)
        """
        r = self._bin_color_to_int(self.r)
        g = self._bin_color_to_int(self.g)
        b = self._bin_color_to_int(self.b)

        return r, g, b

    def __str__(self):
        return f"red: {self.r}, green: {self.g}, blue: {self.b}"


def str_to_bits(text: str) -> list[Literal["0"] | Literal["1"]]:
    text = text + END_OF_MESSAGE_SIGN
    text = text.encode("ascii")  # encode to bytes
    text = [bin(byte) for byte in text]  # cast bytes to bits
    text = [
        byte[2:].zfill(8) for byte in text
    ]  # trim header '0b' and fill leading zeros
    text = list(chain(*text))  # unpack nested strs
    text.extend([])

    return text


def bits_to_str(bits: Annotated[list[str], 8]) -> str:
    text = list()
    cache = dict()

    for byte in bits:
        if byte in cache:
            text.append(cache[byte])
        else:
            character = chr(int(byte, 2))
            cache[byte] = character
            text.append(character)

        try:
            if text[-END_OF_MESSAGE_SIGN_LENGTH:] == END_OF_MESSAGE_SIGN_LIST:
                break
        except IndexError:
            continue

    text: str = "".join(text[:-4])
    return text


def pack_up_bits(bits: list[0 | 1]) -> Annotated[list[str], 8]:
    bits_groupped = list()

    for n in range(0, len(bits), 8):
        byte = bits[n : n + 8]
        bits_groupped.append("".join(byte))

        if len(bits_groupped[-1]) != 8:
            bits_groupped.pop()

    return bits_groupped


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


def hide(img: Image, text: str):
    text: list[Literal["0"] | Literal["1"]] = str_to_bits(text)
    img = encode_bits(img, text)

    return img


def encode_bits(img: Image, bits: list[Literal["0"], Literal["1"]]) -> Image:
    pixels = img.load()
    height, width = img.height, img.width

    if len(bits) % 8 != 0:
        raise InvalidBitsError

    if height * width * 3 < len(bits) + END_OF_MESSAGE_SIGN_LENGTH * 8:
        raise TooSmallImageError

    bits = bits[::-1]

    for x, y in product(range(width), range(height)):
        pixel = Pixel(*pixels[x, y])

        try:
            pixel.r[-1] = bits.pop()
            pixel.g[-1] = bits.pop()
            pixel.b[-1] = bits.pop()
        except IndexError:
            break
        finally:
            pixels[x, y] = pixel.get_color()

    return img


def open_bmp(filename: str):
    if not filename.endswith(".bmp"):
        raise InvalidImageExtensionError

    img = Image.open(filename)

    return img


def extract_usefull_bits(img) -> list[0 | 1]:
    pixels = img.load()
    height, width = img.height, img.width

    bits = list()
    for x, y in product(range(width), range(height)):
        pixel = Pixel(*pixels[x, y])
        bits.extend((pixel.r[-1], pixel.g[-1], pixel.b[-1]))

    return bits


def show(filename: str) -> str:
    img = open_bmp(filename)
    bits: list[0 | 1] = extract_usefull_bits(img)
    bits: Annotated[list[str], 8] = pack_up_bits(bits)
    text = bits_to_str(bits)

    return text


if __name__ == "__main__":
    # painter = Painter(1000, 500)
    # img = painter.draw("sinusoidal")
    # text: str = "some text to hide in new image with size 100 x 500 updated with end"
    # img_crypted = hide(img, text)

    # img_crypted.save("test.bmp")

    text = show("test.bmp")
    print(text)
