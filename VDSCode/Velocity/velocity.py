import time
import sys
import math
import threading
import multiprocessing
sys.path.insert(1,'/home/pi/Desktop/VDS_3.0/VDSCode/DAQ/PressureSensor')
import BMP280
sys.path.insert(1,'/home/pi/Desktop/VDS_3.0/VDSCode/DAQ/VectorNav')
#import vectornavLib
sys.path.insert(1,'/home/pi/Desktop/VDS_3.0/VDSCode/Data')
import RocketConstants as rocket

b=BMP280.BMP()
G=9.8
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
        
        x = 1 - exp(-2 * rocket.minC *(rocket.targetAlt - alt))
        if (x < 0):
            x = 0
        if (vel < rocket.interVel):
            returnVal = velocity_h(rocket.min, alt, 0, rocket.targetAlt)
        elif (vel >= rocket.interVel):
            if (alt < rocket.targetAlt):
                returnVal = velocity_h(rocket.Cspp, alt, rocket.interVel, rocket.interAlt)
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
        
        K1 = (-1 / math.sqrt(c*G)) * math.atan(v0*math.sqrt(c / G))
        K2 = h0 - (1 / c)*math.log(math.cos((math.sqrt(c*G)) * K1))
        x = 1 - math.exp(-2 * c*(K2 - alt))
        
        if (x < 0):
            x = 0
    
        return math.exp(c*(K2 - alt))*math.sqrt(G / c)*math.sqrt(x)
