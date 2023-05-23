from typing import (
    Annotated,
    Literal,
)
from itertools import chain


class BinaryHandler:
    def __init__(self, end_of_message_sign):
        self._end_of_message_sign = end_of_message_sign
        self._end_of_message_sign_length = len(end_of_message_sign)
        self._end_of_message_sign_list = list(end_of_message_sign)

    def str_to_bits(self, text: str) -> list[Literal["0"] | Literal["1"]]:
        text = text + self._end_of_message_sign
        text = text.encode("ascii")  # encode to bytes
        text = [bin(byte) for byte in text]  # cast bytes to bits
        text = [
            byte[2:].zfill(8) for byte in text
        ]  # trim header '0b' and fill leading zeros
        text = list(chain(*text))  # unpack nested strs
        text.extend([])

        return text

    def bits_to_str(self, bits: Annotated[list[str], 8]) -> str:
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
                if (
                    text[-self._end_of_message_sign_length :]
                    == self._end_of_message_sign_list
                ):
                    break
            except IndexError:
                continue

        text: str = "".join(text[:-4])
        return text

    def pack_up_bits(self, bits: list[0 | 1]) -> Annotated[list[str], 8]:
        """transforms raw sequence of bits into list with 8 bit strings"""
        bits_groupped = list()

        for n in range(0, len(bits), 8):
            byte = bits[n : n + 8]
            bits_groupped.append("".join(byte))

            if len(bits_groupped[-1]) != 8:
                bits_groupped.pop()

        return bits_groupped
