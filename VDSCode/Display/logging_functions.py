import serial
import time
import math
import numpy as np
import adafruit_bmp280
import busio
import board
import matplotlib.pyplot as plt

gpsData = "0,0,0"

# initialize the serial port for the GPS
imu = serial.Serial(
    port='/dev/ttyUSB0',  # ttyS0/ttyAMA0 for the serial line and ttyUSB0 for the usb port
    baudrate=115200,  # different baud rates include 4600,9600,115200
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

i2c = busio.I2C(board.SCL, board.SDA)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x77)  # .pressure and .altitude
bmp280.seaLevelhPa = bmp280.pressure

class logging:
    def alt(self):
        f = open("/home/pi/Desktop/VDS_3.0/VDSCode/LOGS/ALT_LOG.txt", "a")
        f.write(str(bmp280.altitude))
        f.close()

    def gps(self):
        while 1:
            f = open("GPS_LOG.txt", "a")
            f.write("gps data goes here")
            f.close()

    def imu(self):
        while 1:
            f = open("IMU_LOG.txt", "a")
            while imu.inWaiting() == 0:
                pass
            dataVar = imu.readline()
            dataVar = str(dataVar, 'utf-8')  # remove b''
            f.write(str(dataVar))
            f.close()