import serial
import time
import math
import numpy as np
import adafruit_bmp280
import busio
import board
import matplotlib.pyplot as plt

gpsData = "0,0,0"

#initialize the serial port for the GPS
imu = serial.Serial(
        port='/dev/ttyUSB0',# ttyS0/ttyAMA0 for the serial line and ttyUSB0 for the usb port
        baudrate = 115200,#different baud rates include 4600,9600,115200
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1 
)

i2c = busio.I2C(board.SCL, board.SDA)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x77)   #.pressure and .altitude 
bmp280.seaLevelhPa = bmp280.pressure

def gravVectCalc():
    #This sees if data is not inbound then nothing happens (the pass)
    while(imu.inWaiting() == 0):
        pass
    
    dataVar = imu.readline()
    dataVar = str(dataVar, 'utf-8') #remove b''
    splitData = dataVar.split(',') #Store data in array after every comma
    
    #if data has 13 values, convert data to radians and store/define yaw, pitch, roll
    if(len(splitData))==13:
        yaw = (math.pi/180)*float(splitData[1])
        pitch = (math.pi/180)*float(splitData[2])
        roll = (math.pi/180)*float(splitData[3])
         
        #Matrix 4: Ressurection (Rotation vector arrays)
        rotGrav = np.array([[0],[0], [-9.8]])
         
        rotYaw = np.array([ [math.cos(yaw), (-1)*math.sin(yaw), 0],
                            [math.sin(yaw), math.cos(yaw), 0],
                            [0, 0, 1] ])
         
        rotPitch = np.array([ [math.cos(pitch), 0, math.sin(pitch)],
                              [0, 1, 0],
                              [(-1)*math.sin(pitch), 0, math.cos(pitch)] ])
         
        rotRoll = np.array([ [1, 0, 0],
                             [0, math.cos(roll), (-1)*math.sin(roll)],
                             [0, math.sin(roll), math.cos(roll)] ])
         
        rotTotal = np.dot(rotYaw,rotPitch,rotRoll) #Dot product the 3 main
         
        gravVect = np.dot(rotTotal, rotGrav) # Return gravity vector
        return gravVect
    


while 1:
    gravVect = gravVectCalc()
    print(gravVect)
    print(bmp280.pressure, " | " , bmp280.altitude)