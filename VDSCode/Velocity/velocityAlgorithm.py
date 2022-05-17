import sys
import time
import threading
import numpy as np
import matplotlib as plt
import math

sys.path.insert(1,'/home/pi/Desktop/VDS_3.0/VDSCode/DAQ/PressureSensor')
import BMP280
sys.path.insert(1,'/home/pi/Desktop/VDS_3.0/VDSCode/DAQ/VectorNav')
import vectornavLib

v=vectornavLib.vnav()
b=BMP280.BMP()

mx,my,mz,bx,by,bz = (.872119572,1.018324019,1.014378100,-0.322006014,0.389388085,1.737349769)


altitude=b.readBMP()
#     print(altitude)
while(1):
    raw=v.readVnav()
    #print(raw)
    zAccel = round(float(raw[9])*mz + bz,3)
    xAccel = round(float(raw[7])*mx + bx,3)
    yAccel = round(float(raw[8])*my + by,3)
    pitch = abs(float(raw[2]))
    roll  = abs(float(raw[3]))
    if(pitch > 90 or roll > 90):
        print("invalid")
        break 
    pitch = (90 - pitch)*(math.pi/180)
    roll  = (90 - roll)*(math.pi/180)
    
    pitchOffset = math.cos(pitch)
    rollOffset  = math.cos(roll)
    PercentVertical = (math.sqrt(abs(1-(pitchOffset**2)-(rollOffset**2))) / 1 )
    #print(pitchOffset,rollOffset)
    #print("Vertical Acceleration:  " + str(round(PercentVertical,3)*(zAccel+9.8)))    
    #finalArray = np.dot(tempAccelArray,gravityvectorRocket)
    #print(str(finalArray))
    #print(zMeasured)
    
    print("yaw:  " + str(raw[1]) + "  pitch:  "+ str(raw[2]) + "  roll:  "+ str(raw[3]) + "  xAccel:" + str(xAccel) + "  yAccel:"+ str(yAccel) +"  zAccel"+ str(zAccel))
    #print( "x:   " + str(gravityvectorRocket[0]) +  "y:   " + str(gravityvectorRocket[1]) +  "  z:   " + str(gravityvectorRocket[2]))
#mx,my,mz,bx,by,bz = v.gradientDecent()

def calulateVelocity():
    #Variables needed for caluation
    sumBMPTimes = 0
    sumBMPTimes2 = 0
    sumAlt = 0
    sumAltTimes = 0
    leftSide = 0
    rightSide = 0
    
    #Find sums for BMP
    for i in range(0, NUM_ALT_READINGS):
        sumBMPTimes += BMPTimes[i]

        sumBMPTimes2 += (BMPTimes[i]**2)
        sumAlt += altitudes[i]
        sumAltTimes += (altitudes[i] * BMPTimes[i])        

    #Calulate left side of equation
    leftSide =  ((sumBMPTimes * sumAlt) - (NUM_ALT_READINGS * sumAltTimes)) / (((sumBMPTimes)**2) - (NUM_ALT_READINGS* sumBMPTimes2))

    #Calculate rightSide of equation
    for i in range((int(NUM_ACCEL_READINGS/2)),(NUM_ACCEL_READINGS-1),1):
        rightSide += (.5*(accelerationFromBNO[i] + accelerationFromBNO[i+1])*(BNOTimes[i+1]-BNOTimes[i]))

    return (leftSide + rightSide)


NUM_ACCEL_READINGS = 10
NUM_ALT_READINGS = 10

run = False #set True to run the main stuff

accelerationFromBNO = list(range(0,NUM_ACCEL_READINGS))
BNOTimes = list(range(0,NUM_ACCEL_READINGS))
altitudes = list(range(0,NUM_ALT_READINGS))
BMPTimes = list(range(0,NUM_ALT_READINGS))
def current_seconds_time():
    return round(time.time())
while run:
        
    currentTime = current_seconds_time()
    for i in range (NUM_ALT_READINGS,0,-1):
        
        newTime = current_seconds_time() - currentTime
        
        raw=v.readVnav()
        
        #print(float(raw[9]))
        accelerationFromBNO.insert(0,(mz*float(raw[9])+bz) + 9.8) # insert '(mz*float(raw[9])+bz) + 9.8' for the '0'
        BNOTimes.insert(0,int(newTime))
        altitudes.insert(0,float(b.readBMP()))
        BMPTimes.insert(0,int(newTime))


    altitudes.insert(0,altitudes.pop())
    altitudes[0]=b.readBMP()
    #for i in range(0,NUM_ACCEL_READINGS,1):
        #print("{0}, {1}, {2}, {3}".format(accelerationFromBNO[i], BNOTimes[i], altitudes[i], BMPTimes[i]))
        
    print("Final Velocity = {}".format(calulateVelocity()))

    #run = False