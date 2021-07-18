import adafruit_ssd1306
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import time

# Setup i2c bus  sudo i2cdetect -y 1
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
display.fill(0)
display.show()
width = display.width
height = display.height

class oled():
    def displayStats(self):
        display.text('RX: ', 0, 0, 1)
        display.show()
        time.sleep(.5)
        display.fill(0) 
        display.show()
    
