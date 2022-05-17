import time
import math
import matplotlib.pyplot as plt

import RocketConstants as rocket
import PressureSensor.BMP280

p = PressureSensor.BMP280.BMP()
G=9.8

DEBUG=1
bmpStarted=0
while not bmpStarted:
    try:

        import AccelerationSensor.BNO055
        ASensor =  AccelerationSensor.BNO055.BNO()
        Accel, dt = ASensor.getVertAccel()
        bmpStarted=1
        print("started")
    except:
        print('oops')
        continue

class velocity():
#  /**************************************************************************/
#  /*!
#  @brief  Velocity of the Set Point Path (SPP). Returns a velocity at which the vehicle should be moving for a given
#  altitude argument. The SPP is also piecewise.
#  Author: Ben
#  */
#  /**************************************************************************/
    
    def vSPP(self, alt, vel):
        
        global returnVal, x
        
        x = 1 - math.exp(-2 * rocket.cMin *(rocket.targetAlt - alt))
        if (x < 0):
            x = 0
        if (vel < rocket.interVel):
            returnVal = self.velocity_h(rocket.cMin, alt, 0, rocket.targetAlt)
        elif (vel >= rocket.interVel):
            if (alt < rocket.targetAlt):
                returnVal = self.velocity_h(rocket.Cspp, alt, rocket.interVel, rocket.interAlt)
            else:
                returnVal = 0    
        else: 
            returnVal = 0
        return returnVal

        if DEBUG_V_SPP:
            print("");
            print("vSPP------------------")
            print("x: ")
            print(x)
            print("h0:")
            print(h0)
            print("vSPP: ")
            print(returnVal)

#/**************************************************************************/
#/*!
#@brief  Calculates velocity as a function of altitude
#Author: Ben
#*/
#/**************************************************************************/
    
    def velocity_h(self, c, alt, v0, h0): 
        
        K1 = -1 / math.sqrt(c*G) * math.atan(v0*math.sqrt(c / G))
        
        K2 = h0 - 1 / c*math.log(math.cos(math.sqrt(c*G) * K1))
        x = 1 - math.exp(-2 * c*(K2 - alt))
        
        if (x < 0):
            x = 0
        v = math.exp(c*(K2 - alt))*math.sqrt(G / c)*math.sqrt(x)
        
        if DEBUG==0:
            print(K1)
            print(K2)
            print(x)
            print()
        return v
    
    def getVelocitySPP(self):\
        print("nothing here yet")
            
if DEBUG ==1:
    v=velocity()
    minCdVel=[0]*rocket.targetAlt
    maxCdVel=[0]*rocket.targetAlt
    sppCdVel=[0]*rocket.targetAlt
    
    for i in range(1,rocket.targetAlt):
        minCdVel[i]=v.velocity_h(rocket.cMin, i, 0, rocket.targetAlt)
        maxCdVel[i]=v.velocity_h(rocket.cMax, i, 0, rocket.targetAlt)
        sppCdVel[i]=v.vSPP(i,130)
    plt.title("Set-Point Path Algorithm")
    plt.xlabel("Altitude (m)")
    plt.ylabel("Vertical Velocity (m/s)")
    
    plt.plot(minCdVel, label="Minimum Drag Characteristic")
    plt.plot(maxCdVel, label="Maximum Drag Characteristic")
    plt.plot(sppCdVel, label="SPP Drag Characteristic")
    plt.legend()
    plt.show()
        