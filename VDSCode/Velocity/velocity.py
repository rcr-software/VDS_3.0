import time
import sys
import math

sys.path.insert(1,'/home/pi/Desktop/VDS3.0/VDSCode/PressureSensor')
import BMP280

b=BMP280.BMP()

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
        
        x = 1 - exp(-2 * rocket.Cmin *(rocket.targetAlt - alt))
        if (x < 0):
            x = 0
        if (vel < rocket.interVel):
            returnVal = velocity_h(rocket.Cmin, alt, 0, rocket.targetAlt)
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
            print("h0: ")
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
        global K1, K2, x
        K1 = -1 / math.sqrt(c*G)ome
        *math.atan(v0*math.sqrt(c / G))
        K2 = h0 - 1 / c*math.log(math.cos(math.sqrt(c*G)*K1))
        x = 1 - math.exp(-2 * c*(K2 - alt))
        
        if (x < 0):
            x = 0
    
        return math.exp(c*(K2 - alt))*math.sqrt(G / c)*math.sqrt(x)
