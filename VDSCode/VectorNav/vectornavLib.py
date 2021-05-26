import time
import serial
import numpy
from threading import Thread

vNavFile = open("vnav.txt","a")

#initialize the serial port for the vectornav
ser = serial.Serial(
        port='/dev/ttyUSB0',# ttyS0 for the serial line and ttyUSB0 for the usb port
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1 
)

class vnav():
    def readVnav(self):
        while True:
            vertVel=0

            vertVel = float(vertVel)
            startTime = time.time()
        
            x = str(ser.readline())
            x = x.split(',')
           
            if(len(x) == 13):
                Accelx = float(x[7])
                Accely = float(x[8])
                Accelz = float(x[9])
            
                Ax = Accelx / (((Accelx**2)+(Accely**2)+(Accelz**2))**.5) #calculate the normal vector
                Ay = Accely / (((Accelx**2)+(Accely**2)+(Accelz**2))**.5)
                Az = Accelz / (((Accelx**2)+(Accely**2)+(Accelz**2))**.5)
            
            
                R0 = ((Ay**2)-(Ax**2)*(Az))/((Ax**2)+(Ay**2))  #calculate the rotation matrix
                R1 = ((-1*Ax*Ay)-(Ax*Ay*Az))/((Ax**2)+(Ay**2))
                R2 = Ax
                R3 = ((-1*Ax*Ay)-(Ax*Ay*Az))/((Ax**2)+(Ay**2))
                R4 = ((Ax**2)-((Ay**2)*(Az)))/((Ax**2)+(Ay**2))
                R5 = Ay
                R6 = -1*Ax
                R7 = -1*Ay
                R8 = -1*Az
            
                RotationMatrix = numpy.array(((R0,R1,R2), (R3,R4,R5), (R6,R7,R8)))
                accelVector = numpy.array(((Accelx),(Accely),(Accelz)))
            
                mul = numpy.dot(RotationMatrix, accelVector)
                mul[0] = round(mul[0],1)
                mul[1] = round(mul[1],1)

                vertAccel = mul[2]+9.8
                endTime = time.time()
            
                timeElapsed = startTime-endTime
                vertVel = round(vertVel + vertAccel*timeElapsed,2)
                vertVel = str(vertVel)
                        
                vNavFile.write(str(vertVel))
                vNavFile.write('\n')
                
                print(x[1])
                ser.flushInput()
                
                
                time.sleep(1)
        
    def vnavTxtClose(self):
        vNavFile.close()