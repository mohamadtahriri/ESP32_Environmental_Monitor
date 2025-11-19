# lcd_api.py - Abstract class for LCD devices (MicroPython)
import utime

class LcdApi:
    """Abstract base class for character LCD devices."""

    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.row_offsets = (0x00, 0x40, 0x14, 0x54)
        if num_rows > 4:
            raise ValueError("Too many rows")

    def clear(self):
        self.command(0x01)
        self.delay_ms(2)

    def home(self):
        self.command(0x02)
        self.delay_ms(2)

    def move_to(self, col, row):
        self.command(0x80 | (col + self.row_offsets[row]))

    def putstr(self, string):
        for char in string:
            self.character(ord(char))

    def character(self, code):
        raise NotImplementedError

    def command(self, code):
        raise NotImplementedError

    def delay_ms(self, ms):
        utime.sleep_ms(ms)