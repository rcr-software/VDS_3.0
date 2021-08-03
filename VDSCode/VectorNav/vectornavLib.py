import time
import serial
import numpy
from threading import Thread
import math
import sympy
import numpy as np
import matplotlib.pyplot as plt
from sympy.abc import x as a,y as b, z as c
import sys

vNavFile = open("vnav.txt","a")

#initialize the serial port for the vectornav
ser = serial.Serial(
        port='/dev/serial0',# ttyS0 for the serial line and ttyUSB0 for the usb port
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1 
)

class vnav():
    threadStopFlag=True
    x= [1] * 13
    vnavMessage=[1] * 13
    gravityVectorRocket=[1] * 3
    
    def runThread(self,stopFlag):
        self.threadStopFlag=stopFlag
        return(stopFlag)
    
    def readVnav(self):
        while self.threadStopFlag:
            ser.flushInput()
            self.x = str(ser.readline())
            self.x = self.x.split(',')              
            if(len(self.x) == 13):
                vNavHeader = "b'$VNYMR" in self.x
                if(vNavHeader==1):
                    self.vnavMessage=self.x
                    self.getGravityVector()            
                    
                    #print(self.vnavMessage)
            time.sleep(.1)
    def calculateVericalAccel(self):
        while self.threadStopFlag:
            startTime = time.time()
            vertVel=0
            Accelx = float(self.vnavMessage[7])
            Accely = float(self.vnavMessage[8])
            Accelz = float(self.vnavMessage[9])
            
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
            vertAccel = mul[2]+9.81
            #print(vertAccel)
            
            endTime = time.time()
            timeElapsed = startTime-endTime
            vertVel = round(vertVel + vertAccel*timeElapsed,2)
                        
            time.sleep(.5)
            # vNavFile.write(str(vertVel))
           # vNavFile.write('\n')
    def getGravityVector(self):
        yaw = float(self.vnavMessage[1])
        pitch = float(self.vnavMessage[2])
        roll = float(self.vnavMessage[3])
        
        rYaw=yaw     *(math.pi/180) #convert from degrees to radians
        rPitch=pitch *(math.pi/180)
        rRoll=roll   *(math.pi/180)
        gravityVectorEarth = numpy.array(((0), (0), (9.81)))
        
        yaw0=math.cos(rYaw)
        yaw1=-1*math.sin(rYaw)
        yaw2=0
        yaw3=math.sin(rYaw)
        yaw4=math.cos(rYaw)
        yaw5=0
        yaw6=0
        yaw7=0
        yaw8=1
        yawRotationMatrix = numpy.array(((yaw0,yaw1,yaw2), (yaw3,yaw4,yaw5), (yaw6,yaw7,yaw8)))
        
        pitch0=math.cos(rPitch)
        pitch1=0
        pitch2=math.sin(rPitch)
        pitch3=0
        pitch4=1
        pitch5=0
        pitch6=-1*math.sin(rPitch)
        pitch7=0
        pitch8=math.cos(rPitch)
        pitchRotationMatrix = numpy.array(((pitch0,pitch1,pitch2), (pitch3,pitch4,pitch5), (pitch6,pitch7,pitch8)))
        
        roll0=1
        roll1=0
        roll2=0
        roll3=0
        roll4=math.cos(rRoll)
        roll5=-1*math.sin(rRoll)
        roll6=0
        roll7=math.sin(rRoll)
        roll8=math.cos(rRoll)
        rollRotationMatrix = numpy.array(((roll0,roll1,roll2), (roll3,roll4,roll5), (roll6,roll7,roll8)))
        
        self.gravityVectorRocket= numpy.dot(numpy.dot(numpy.dot(pitchRotationMatrix, yawRotationMatrix), rollRotationMatrix),gravityVectorEarth)
        return self.gravityVectorRocket
        #print(gravityVectorRocket)   
    def vnavTxtClose(self):
        vNavFile.close()

    def gradientDecent(self):
        samples = 100
        alpha = .0001
        
        xMeasured = [0]*samples
        yMeasured = [0]*samples
        zMeasured = [0]*samples
        xActual   = [0]*samples
        yActual   = [0]*samples
        zActual   = [0]*samples
        
        #get a list of data points for each axis
        time.sleep(1)#wait for vnav to start
        for i in range(samples):
             xMeasured[i] = float(self.vnavMessage[7])
             yMeasured[i] = float(self.vnavMessage[8])
             zMeasured[i] = float(self.vnavMessage[9])
             print(xMeasured[i])
             
             xActual[i]   = float(self.gravityVectorRocket[0])
             yActual[i]   = float(self.gravityVectorRocket[1])
             zActual[i]   = -1*float(self.gravityVectorRocket[2])
             print(xActual[i])
             time.sleep(.1)
             
        xMeasured = np.array(xMeasured)
        yMeasured = np.array(yMeasured)
        zMeasured = np.array(zMeasured)
        xActual   = np.array(xActual)
        yActual   = np.array(yActual)
        zActual   = np.array(zActual)
        
        mx, my, mz, bx, by, bz = sympy.symbols('mx my mz bx by bz')
        mx, my, mz, bx, by, bz = 0, 0, 0, 0, 0, 0
        fig = plt.figure()
        
        plt.plot(xMeasured,xActual)
        plt.xlabel="Actual Gravity Acceleration"
        plt.ylabel="Measured Gravity Acceleration"
        plt.show()
        for i in range(10000):
            mx -= alpha*np.sum((mx*xActual+bx-xMeasured)*xActual)
            #my -= alpha*np.sum((my*yMeasured+by-yActual)*yMeasured)
            #mz -= alpha*np.sum((mz*zMeasured+bz-zActual)*zMeasured)
            bx -= alpha*np.sum(bx*xActual+bx-xMeasured)
            #by -= alpha*np.sum(by*yMeasured+by-yActual)
            #bz -= alpha*np.sum(bz*zMeasured+bz-zActual)
        print("slopes and intercepts")    
        print(mx)
        #print(my)
        #print(mz)
        print(bx)
        
        x = np.linspace(-9.8, 9.8, num=samples)
        y=x*mx+bx
        
        
        #print(by)
        #print(bz)