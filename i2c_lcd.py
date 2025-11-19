# i2c_lcd.py - I2C LCD driver for PCF8574 (MicroPython)
from machine import I2C, Pin
from lcd_api import LcdApi
import utime

class I2cLcd(LcdApi):
    """Driver for PCF8574-based I2C LCD modules."""
    
    LCD_I2C_BL = 0x08  # Backlight enable bit

    def __init__(self, i2c, i2c_addr, num_rows, num_cols):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.i2c.scan()
        self.i2c.writeto(self.i2c_addr, bytes([0x00]))
        
        super().__init__(num_rows, num_cols)
        self.display_init()

    def display_init(self):
        self.delay_ms(20)
        self.write_nibble(0x03)
        self.delay_ms(5)
        self.write_nibble(0x03)
        self.delay_us(100)
        self.write_nibble(0x03)
        self.delay_us(100)
        self.write_nibble(0x02) # Set 4-bit mode
        self.command(0x28) # 4-bit, 2-line, 5x8 dots
        self.command(0x0C) # Display on, Cursor off, Blink off
        self.command(0x06) # Entry mode set
        self.clear()

    def write_nibble(self, nibble, mode=0):
        data = (nibble << 4) & 0xF0
        
        # Send first (enable=1)
        self.i2c.writeto(self.i2c_addr, bytes([data | mode | self.LCD_I2C_BL | 0x04])) 
        self.delay_us(1)
        
        # Send second (enable=0)
        self.i2c.writeto(self.i2c_addr, bytes([data | mode | self.LCD_I2C_BL]))
        self.i2c.writeto(self.i2c_addr, bytes([data | mode | self.LCD_I2C_BL])) # Ensure RW is low

    def command(self, cmd):
        self.write_nibble(cmd >> 4, 0)
        self.write_nibble(cmd & 0x0F, 0)

    def character(self, char_code):
        self.write_nibble(char_code >> 4, 1)
        self.write_nibble(char_code & 0x0F, 1)
        
    def delay_us(self, us):
        utime.sleep_us(us)