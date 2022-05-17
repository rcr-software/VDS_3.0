import PressureSensor.BMP280 as BMP280
import AccelerationSensor.BNO055 as BNOcode

PSensor = BMP280.BMP()
ASensor =  BNOcode.BNO()

while 1:
    Alt = PSensor.readBMP()
    #print(Alt)
    Accel, dt = ASensor.getVertAccel() 
    #print("Accel: {}".format(Accel))
    #print("dt: {}".format(dt))
