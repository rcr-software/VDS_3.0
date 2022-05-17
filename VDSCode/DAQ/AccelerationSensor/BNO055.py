#authors-Roger and Abel
import logging
import sys
import time
import multiprocessing
from Adafruit_BNO055 import BNO055

#vin-5v/3.3v
#gnd-gnd
#sda-rxd
#scl-txd
#ps1-5v/3.3v
#rst-any gpio (pin 18 in our example)

bno = BNO055.BNO055(serial_port='/dev/ttyUSB0', rst=18) #Set serial port to ttyUSB0 due to the fact we are running UART over I2C.
logging.basicConfig(filename=__name__,level=logging.DEBUG)

class BNO():
    global Ready
    # threadStopFlag = True
    if not bno.begin():
        raise RuntimeError('Failed to initialize BNO055! Is the sensor connects?')
    
    def initialize(self):
        # Our goal is to rerun this script every single time that error occurs.
        # The best fix is to initialize the code until the error no longer shows up.
        print('BNO055 has been successfully initialized!')

    
#     def runThread(self,stopFlag):
#         self.threadStopFlag=stopFlag
#         return(stopFlag)
    
    def runProcess(self):
        self.vertaccelprocc = multiprocessing.Process(target = BNO.getVertAccel, args=(self,))
        print('Vertical acceleration process initialized!')
        self.vertaccelprocc.start()
        print('Vertical acceleration process up and running!')
    
    def killProcess(self):
        self.vertaccelprocc.terminate()
        print('Vertical acceleration process terminated successfully!')

    def getSysStatus():
        status, self_test, error = bno.get_system_status()
        print ('System status: {0}'.format(status))
        print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
        # Print out an error if system status is in error mode.
        if status == 0x01:
            print('System error: {0}'.format(error))
            print('See datasheet section 4.3.59 for the meaning.')

        sw, bl, accel, mag, gyro = bno.get_revision()
        print('Software version:   {0}'.format(sw))
        print('Bootloader version: {0}'.format(bl))
        print('Accelerometer ID:   0x{0:02X}'.format(accel))
        print('Magnetometer ID:    0x{0:02X}'.format(mag))
        print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

    def testCalibration(self):  # DELETE SELF IF BROKEN
        sys, gyro, accel, mag = bno.get_calibration_status() # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
        if(sys<3):
            logging.info("sys is not callibrated")
        if(gyro<3):
            logging.info("gyroscope is not callibrated")
        if(accel<3):
            logging.info("acceleromter is not callibrated")
        if(mag<3):
            logging.info("magnometer is not callibrated")
            
    
    def getVertAccel(self):  # DELETE SELF IF BROKEN
        while 1:
            start = time.time()
            
            self.testCalibration()
            verticalAcceleration=0
            
            xl,yl,zl = bno.read_linear_acceleration() # Linear acceleration data (i.e. acceleration from movement, not gravity returned in meters per second squared):
            xg,yg,zg = bno.read_gravity() # Gravity acceleration data (i.e. acceleration just from gravity--returned in meters per second squared):
            try:
                linearDotGrav=xl*xg +yl*yg + zl*zg
                magL=(xl**2 + yl**2 + zl**2)**.5
                magG=(xg**2 + yg**2 + zg**2)**.5
                verticalAcceleration=linearDotGrav / magG
            except ZeroDivisionError:
                logging.exception("Division by Zero Error")

            time.sleep(0.01)
            end = time.time()
            dt = (end - start)
            print(f'Vertical acceleration is: {verticalAcceleration}.')
            time.sleep(1)
            return verticalAcceleration, dt
    

#while 1:
#    print(getVertAccel())

#x,y,z,w = bno.read_quaterion() # Orientation as a quaternion:
#temp_c = bno.read_temp() # Sensor temperature in degrees Celsius:
#x,y,z = bno.read_magnetometer() # Magnetometer data (in micro-Teslas):
#x,y,z = bno.read_gyroscope() # Gyroscope data (in degrees per second):
#x,y,z = bno.read_accelerometer() # Accelerometer data (in meters per second squared):
#heading, roll, pitch = bno.read_euler() # Read the Euler angles for heading, roll, pitch (all in degrees).
o = BNO()
o.runProcess()