import adafruit_bmp280
import numpy as np
import busio
import board
import matplotlib.pyplot as plt
import time

# intial kalman parameters################
n = 500000
sz = (n) # size of array
t = np.linspace(0,10,n)
x = t # truth function
z= np.zeros(sz) # noisy altitude readings
Q = 1e-4 # process variance


# allocate space for arrays
xhat=np.zeros(sz)      # a posteri estimate of x
P=np.zeros(sz)         # a posteri error estimate
xhatminus=np.zeros(sz) # a priori estimate of x
Pminus=np.zeros(sz)    # a priori error estimate
K=np.zeros(sz)         # Kalman gain
R = 0.1**2 # estimate of measurement variance
xhat[0] = 0.0
P[0] = 1.0

# Setup i2c bus  sudo i2cdetect -y 1
i2c = busio.I2C(board.SCL, board.SDA)
# BMP280 1
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x77)
bmp280.seaLevelhPa = bmp280.pressure

global j
j=0

class BMP():
    def __init__(self):
        self.z=z    

    def readBMP(self):
        while 1:
            global j, bmp280Alt
               
            j=j+1
            z[j]=bmp280.altitude-170
            bmp280Alt = z[j]
            print(z[j])  #Prints altitude                     

        
            xhatminus[j] = xhat[j-1]
            Pminus[j] = P[j-1]+Q


            K[j] = Pminus[j]/( Pminus[j]+R )
            xhat[j] = xhatminus[j]+K[j]*(z[j]-xhatminus[j])
            P[j] = (1-K[j])*Pminus[j]
            
            return self.z[j]
            time.sleep(1)
            
#display the kalman filtered altitude readings
    def plotBMP():
        
        plt.figure()
        plt.plot(t, z,'k+',label='noisy measurements')
        plt.plot(t, xhat,'b-',label='a posteri estimate')
        plt.plot(t,x,color='g',label='truth value')
        plt.legend()
        plt.xlabel('t')
        plt.ylabel('f(t)')
        plt.show()
