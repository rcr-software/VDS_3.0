import adafruit_bmp280
import numpy as np
import time
import math
import busio
import board
import matplotlib.pyplot as plt

# Setup i2c bus  sudo i2cdetect -y 1
i2c = busio.I2C(board.SCL, board.SDA)
# BMP280 1
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x77)
bmp280.seaLevelhPa = bmp280.pressure

while 1:
    time.sleep(2)
    print(bmp280.pressure, " | " , bmp280.altitude)
    