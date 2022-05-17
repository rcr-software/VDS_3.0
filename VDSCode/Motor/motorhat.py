
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for using adafruit_motorkit with a DC motor"""
import time
import board
from adafruit_motorkit import MotorKit

kit = MotorKit(i2c=board.I2C())



class motor:
    def inchout(self):
        kit.motor3.throttle = -1.0
        time.sleep(.2)
        kit.motor3.throttle = 0
    def inchin(self):
        kit.motor3.throttle = 1.0
        time.sleep(.2)
        kit.motor3.throttle = 0
    def sweep(selfS):
        kit.motor3.throttle = 1.0
        time.sleep(.7)
        kit.motor3.throttle = -1.0
        time.sleep(.7)
        kit.motor3.throttle = 0

