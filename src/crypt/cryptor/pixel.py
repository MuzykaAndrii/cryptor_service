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
