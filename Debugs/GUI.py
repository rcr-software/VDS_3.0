#import Libraries
import math
import time
import threading

import serial
from tkinter import* 
from time import sleep
import RPi.GPIO as GPIO
import numpy

import smbus
import board
import digitalio
from digitalio import DigitalInOut, Direction, Pull
import busio

from picamera import PiCamera
import adafruit_rfm9x
import adafruit_ssd1306
import adafruit_bmp280
import vnpy

import GUI

CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
prev_packet = None

def radioCheck():
    try:
        rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
        display.text('RFM9x: Detected', 0, 0, 1)
    except RuntimeError as error:
    # Thrown on version mismatch
        display.text('RFM9x: ERROR', 0, 0, 1)
        print('RFM9x Error: ', error)
        
    display.show()    
    time.sleep(.1)
    display.fill(0)
    display.show()
    
    