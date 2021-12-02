import serial
import time

gpsData = "0,0,0"

#initialize the serial port for the GPS
imu = serial.Serial(
        port='/dev/ttyUSB0',# ttyS0/ttyAMA0 for the serial line and ttyUSB0 for the usb port
        baudrate = 115200,#different baud rates include 4600,9600,115200
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=None
)

while 1:

  #This sees if data is not inbound then nothing happens (the pass)
  #while(imu.inWaiting() == 0):
    #pass
    imu.flushInput()
    dataVar = imu.readline()
    
  #Removes b'' formatting
    dataVar = str(dataVar, 'utf-8') 
  #Separates each input number at the commas
    splitData = dataVar.split(',')
    time.sleep(.5)
    print(splitData)
  #These are example holders for each index of the split dataVar
#     vinnymr = str(splitData[0]) #Ignore $VNYMR
#     first = str(splitData[1])
#     second = str(splitData[2])
#     third = str(splitData[3])
#     fourth = str(splitData[4])
#     fifth = str(splitData[5])
#     sixth = str(splitData[6])
#   #Print statement 
#     sys.stdout.write("first = " + first + "second = " +second + "third = " + third, "fourth = " + fourth + "fifth = " +fifth + "sixth = " + sixth + "\n")
# 
