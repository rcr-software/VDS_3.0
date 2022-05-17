DEBUG=0

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
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


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
    threadStopFlag=True
    
    x = [1] * 13
    y = 0
    vnavMessage = [1] * 13
    yaw = 0
    pitch = 0
    roll = 0
    gravityVectorRocket=[1] * 3
    vnavText = open("/home/pi/Desktop/VDS_3.0/VDSCode/LOGS/vnav_log.txt", "a")
      
    def runThread(self,stopFlag):
        self.threadStopFlag=stopFlag  
        return(stopFlag)
    
    def readVnav(self):
        ser.flushInput()
        self.x = str(ser.readline())
        self.y = self.x
        self.x = self.x.split(',')
        
        if DEBUG:
            print(self.x)
        
        if(len(self.x) == 13):
            self.vnavText.write(str(self.y) + "\n")
            vNavHeader = "b'$VNYMR" in self.x
            if(vNavHeader==1):
                self.vnavMessage=self.x      
        return self.vnavMessage
            
    def closeVnavTxt(self):
        self.vnavText.close()
        return
        
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
            print(vertAccel)
            
            endTime = time.time()
            timeElapsed = startTime-endTime
            vertVel = round(vertVel + vertAccel*timeElapsed,2)
                        
            time.sleep(.5)
            # vNavFile.write(str(vertVel))
            # vNavFile.write('\n')
    def getGravityVector(self,yaw,pitch,roll):  #gets DIRECTION UNIT VECTOR in direction of gravity
        
        yaw=yaw     *(math.pi/180) #convert from degrees to radians
        pitch=pitch *(math.pi/180)
        roll=roll   *(math.pi/180)
        
        rotGrav = np.array([[1],[0], [0]])#m/s/s
         
        rotYaw = np.array([ [math.cos(yaw), (-1)*math.sin(yaw), 0],
                            [math.sin(yaw), math.cos(yaw), 0],
                            [0, 0, 1] ])
         
        rotPitch = np.array([ [math.cos(pitch), 0, math.sin(pitch)],
                              [0, 1, 0],
                              [(-1)*math.sin(pitch), 0, math.cos(pitch)] ])
         
        rotRoll = np.array([ [1, 0, 0],
                             [0, math.cos(roll), (-1)*math.sin(roll)],
                             [0, math.sin(roll), math.cos(roll)] ])
         
        rotTotal = np.dot(rotYaw,rotPitch,rotRoll) #Dot product the 3 main,rotation matrix
         
        gravVect = np.dot(rotTotal, rotGrav) # Return gravity vector,m/s/s
        
        return gravVect
        #print(gravityVectorRocket)
    def getGravityVector2(self,yaw,pitch,roll):  #gets DIRECTION UNIT VECTOR in direction of gravity
        
        yaw=yaw     *(math.pi/180) #convert from degrees to radians
        pitch=pitch *(math.pi/180)
        roll=roll   *(math.pi/180)
        
        rotGrav = np.array([[1],[0], [0]])#m/s/s
         
        rotYaw = np.array([ [math.cos(roll), (-1)*math.sin(roll), 0],
                            [math.sin(roll), math.cos(roll), 0],
                            [0, 0, 1] ])
         
        rotPitch = np.array([ [math.cos(pitch), 0, math.sin(pitch)],
                              [0, 1, 0],
                              [(-1)*math.sin(pitch), 0, math.cos(pitch)] ])
         
        rotRoll = np.array([ [1, 0, 0],
                             [0, math.cos(yaw), (-1)*math.sin(yaw)],
                             [0, math.sin(yaw), math.cos(yaw)] ])
         
        rotTotal = np.dot(rotYaw,rotPitch,rotRoll) #Dot product the 3 main,rotation matrix
         
        gravVect = np.dot(rotTotal, rotGrav) # Return gravity vector,m/s/s
        
        return gravVect
        #print(gravityVectorRocket)
    def plot(self,x,y,z):


        vectors=np.array([[0,0,0,x,y,z]],dtype = object) 
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for vector in vectors:
            v = np.array([vector[3],vector[4],vector[5]])
            vlength=np.linalg.norm(v)
            ax.quiver(vector[0],vector[1],vector[2],vector[3],vector[4],vector[5],
                    pivot='tail',length=vlength,arrow_length_ratio=0.3/vlength)
        ax.set_xlim([-4,4])
        ax.set_ylim([-4,4])
        ax.set_zlim([-4,4])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        plt.show()
    def getGravityUnitVector(self,yaw,pitch,roll):  #gets DIRECTION UNIT VECTOR in direction of gravity
        
        yaw=yaw     *(math.pi/180) #convert from degrees to radians
        pitch=pitch *(math.pi/180)
        roll=roll   *(math.pi/180)
        
        x = round(math.cos(yaw)*math.cos(pitch),4)
        y = round(math.sin(yaw)*math.cos(pitch),4)
        z = round(math.sin(pitch),4)
        
        #unitVector = np.array([x],[y],[z])
        
        print(x,y,z)
                
    def vnavTxtClose(self):
        vNavFile.close()

    def gradientDecent(self):
        
        samples = 100
        alpha   = .0001#rate at which the gradient desends to the minimum cost function
        
        xMeasured = [0]*samples
        yMeasured = [0]*samples
        zMeasured = [0]*samples
        xActual   = [0]*samples
        yActual   = [0]*samples
        zActual   = [0]*samples
        
        #get a list of data points for each axis
        time.sleep(1)#wait for vnav to start
        for i in range(samples):
            raw=self.readVnav()
            #acceleration readings
            xMeasured[i] = float(raw[7])
            yMeasured[i] = float(raw[8])
            zMeasured[i] = float(raw[9])
            #gyro assumed accelration
            gravityVector= self.getGravityVector(float(raw[1]),float(raw[2]),float(raw[3]))
            xActual[i]   = float(gravityVector[0])
            yActual[i]   = float(gravityVector[1])
            zActual[i]   = -1*float(gravityVector[2])
            #get the measured and actual values in the same direction
            if (xMeasured[i]<0 and xActual[i]>0) or (xMeasured[i]>0 and xActual[i]<0):
                xMeasured[i]=-1*xMeasured[i]
            if (yMeasured[i]<0 and yActual[i]>0) or (yMeasured[i]>0 and yActual[i]<0):
                yMeasured[i]=-1*yMeasured[i]
            if (zMeasured[i]<0 and zActual[i]>0) or (zMeasured[i]>0 and zActual[i]<0):
                zMeasured[i]=-1*zMeasured[i]
                 
#              print(zActual[i], end=" ")
#              print(" ", end=" ")
#              print(zMeasured[i])    
#              print("measured ", end=" ")
#              print("actual")   
            time.sleep(.1)
             
        xMeasured = np.array(xMeasured)
        yMeasured = np.array(yMeasured)
        zMeasured = np.array(zMeasured)
        xActual   = np.array(xActual)
        yActual   = np.array(yActual)
        zActual   = np.array(zActual)
        
        mx, my, mz, bx, by, bz = sympy.symbols('mx my mz bx by bz')
        mx, my, mz, bx, by, bz = 1, 1, 1, 1, 1, 1
        
        for i in range(1000):
            mx -= alpha*np.sum((mx*xMeasured+bx-xActual)*xMeasured)
            my -= alpha*np.sum((my*yMeasured+by-yActual)*yMeasured)
            mz -= alpha*np.sum((mz*zMeasured+bz-zActual)*zMeasured)
            bx -= alpha*np.sum( mx*xMeasured+bx-xActual)
            by -= alpha*np.sum( my*yMeasured+by-yActual)
            bz -= alpha*np.sum( mz*zMeasured+bz-zActual)

#         result1=sympy.solve([
#             np.sum(((mx*xActual+bx-xMeasured)*xActual)),
#             np.sum(( mx*xActual+bx-xMeasured))],[mx,bx])
#         result2=sympy.solve([
#             np.sum(((my*yActual+by-yMeasured)*yActual)),
#             np.sum(( my*yActual+by-yMeasured))],[my,by])
#         result3=sympy.solve([
#             np.sum(((mz*zActual+bz-zMeasured)*zActual)),
#             np.sum(( mz*zActual+bz-zMeasured))],[mz,bz])
#         mx=result1[mx]
#         my=result2[my]
#         mz=result3[mz]
#         bx=result1[bx]
#         by=result2[by]
#         bz=result3[bz]        
        print("slopes and intercepts")    
        print(mx)
        print(my)
        print(mz)
        print(bx)
        print(by)
        print(bz)
        
        x = np.linspace(-9.8, 9.8, num=samples)
        xl=x*mx+bx
        y = np.linspace(-9.8, 9.8, num=samples)
        yl=y*my+by
        z = np.linspace(-9.8, 9.8, num=samples)
        zl=z*mz+bz
        
        plt.figure(figsize=(16,9),dpi=80)
        
        plt.subplot(1,3,1)     
        plt.plot(xMeasured,xActual, 'bo')
        plt.plot(x,xl,"b-",label="X lsrl")
        plt.xlabel("Actual Gravity Acceleration")
        plt.ylabel("Measured Gravity Acceleration")
        
        plt.subplot(1,3,2) 
        plt.plot(yMeasured,yActual, 'ro')
        plt.plot(y,yl,"r-",label="Y lsrl")
        plt.xlabel("Actual Gravity Acceleration")
        plt.ylabel("Measured Gravity Acceleration")
        
        plt.subplot(1,3,3) 
        plt.plot(zMeasured,zActual, 'go')
        plt.plot(z,zl,"g-",label="Z lsrl")
        plt.xlabel("Actual Gravity Acceleration")
        plt.ylabel("Measured Gravity Acceleration")
        
        
        plt.show()
        
        return mx,my,mz,bx,by,bz
    
    
        
        
if DEBUG==True:                
    v=vnav()
    v.readVnav()
