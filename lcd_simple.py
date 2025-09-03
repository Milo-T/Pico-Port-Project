# lcd_simple.py - Simple LCD1602 I2C Library for Pico
import time
from machine import Pin, I2C

class LCD1602:
    def __init__(self, i2c, i2c_addr=0x27): # 0x27 or 0x3F
        self.i2c = i2c
        self.addr = i2c_addr
        self.buf = bytearray(1)
        self.BL_ON = 0x08
        self.BL_OFF = 0x00
        self.ENABLE = 0x04
        self._display_mode = 0x0C  # Display on, cursor off, blink off
        self._init_display()

    def _write_byte(self, b):
        self.buf[0] = b
        self.i2c.writeto(self.addr, self.buf)

    def _write_cmd(self, cmd):
        # Send high nibble
        b = (cmd & 0xF0) | self.ENABLE | self.BL_ON
        self._write_byte(b)
        time.sleep_us(10)
        b &= ~self.ENABLE
        self._write_byte(b)
        time.sleep_us(10)

        # Send low nibble
        b = ((cmd << 4) & 0xF0) | self.ENABLE | self.BL_ON
        self._write_byte(b)
        time.sleep_us(10)
        b &= ~self.ENABLE
        self._write_byte(b)
        time.sleep_us(100)

    def _init_display(self):
        # Initialize the display in 4-bit mode
        time.sleep_ms(50)
        for cmd in [0x33, 0x32, 0x28, 0x0C, 0x06, 0x01]:
            self._write_cmd(cmd)
            time.sleep_ms(5)

    def clear(self):
        self._write_cmd(0x01)
        time.sleep_ms(5)

    def print(self, text):
        for char in text:
            self._write_data(ord(char))

    def _write_data(self, data):
        # Send high nibble
        b = (data & 0xF0) | self.ENABLE | 0x01 | self.BL_ON
        self._write_byte(b)
        time.sleep_us(10)
        b &= ~self.ENABLE
        self._write_byte(b)
        time.sleep_us(10)

        # Send low nibble
        b = ((data << 4) & 0xF0) | self.ENABLE | 0x01 | self.BL_ON
        self._write_byte(b)
        time.sleep_us(10)
        b &= ~self.ENABLE
        self._write_byte(b)
        time.sleep_us(100)

    def set_cursor(self, col, row):
        addr = col + (0x40 * row)
        self._write_cmd(0x80 | addr)
