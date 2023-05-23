from PIL import Image
from random import randint
from itertools import product
from typing import (
    Annotated,
    Literal,
)

from .exceptions import (
    TooSmallImageError,
    InvalidBitsError,
)
from .binary_handler import BinaryHandler
from .pixel import Pixel


END_OF_MESSAGE_SIGN = "/em."
binary_handler = BinaryHandler(END_OF_MESSAGE_SIGN)


def clear_usefull_data(img_path: str):
    img = open_bmp(img)
    height, width = img.height, img.width
    pixels = img.load()

    for x, y in product(range(width), range(height)):
        pixel = Pixel(*pixels[x, y])

        pixel.r[-1] = randint(0, 1)
        pixel.g[-1] = randint(0, 1)
        pixel.b[-1] = randint(0, 1)

    return img


def extract_usefull_bits(img) -> list[0 | 1]:
    pixels = img.load()
    height, width = img.height, img.width

    bits = list()
    for x, y in product(range(width), range(height)):
        pixel = Pixel(*pixels[x, y])
        bits.extend((pixel.r[-1], pixel.g[-1], pixel.b[-1]))

    return bits


def encode_bits(img: Image, bits: list[Literal["0"], Literal["1"]]) -> Image:
    pixels = img.load()
    height, width = img.height, img.width

    if len(bits) % 8 != 0:
        raise InvalidBitsError

    if height * width * 3 < len(bits) + binary_handler._end_of_message_sign_length * 8:
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
    return Image.open(filename)


def hide(img, text: str):
    text: list[Literal["0"] | Literal["1"]] = binary_handler.str_to_bits(text)
    img = encode_bits(img, text)

    return img


def show(filename: str) -> str:
    img = open_bmp(filename)
    bits: list[0 | 1] = extract_usefull_bits(img)
    bits: Annotated[list[str], 8] = binary_handler.pack_up_bits(bits)
    text = binary_handler.bits_to_str(bits)

    return text


if __name__ == "__main__":
    # painter = Painter(1000, 500)
    # img = painter.draw("sinusoidal")
    # text: str = "some text to hide in new image with size 100 x 500 updated with end"
    # img_crypted = hide(img, text)

    # img_crypted.save("test.bmp")

    text = show("test.bmp")
    print(text)
