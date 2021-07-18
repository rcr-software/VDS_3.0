import time
import serial
import numpy
from threading import Thread
import math

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
    def runThread(self,stopFlag):
        self.threadStopFlag=stopFlag
        return(stopFlag)
    
    def readVnav(self):
        while self.threadStopFlag:
            ser.flushInput()
            self.x = str(ser.readline())
            self.x = self.x.split(',')              
            if(len(self.x) == 13):
                #print(self.x)
                
                self.vnavMessage=self.x
                self.getGravityVector(float(self.x[1]),float(self.x[2]),float(self.x[3]))
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
                    

            
            
            time.sleep(.1)
            # vNavFile.write(str(vertVel))
           # vNavFile.write('\n')
    def getGravityVector(self,yaw,pitch,roll):
        rYaw=yaw     *(math.pi/180) #convert from degrees to radians
        rPitch=pitch *(math.pi/180)
        rRoll=roll   *(math.pi/180)
        gravityVectorEarth = numpy.array(((0), (0), (-1*9.81)))
        
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
        
        gravityVectorRocket= numpy.dot(numpy.dot(numpy.dot(pitchRotationMatrix, yawRotationMatrix), rollRotationMatrix),gravityVectorEarth)
        
        #print(gravityVectorRocket)   
        
    def vnavTxtClose(self):
        vNavFile.close()
