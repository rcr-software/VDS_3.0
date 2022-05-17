
#import Libraries
import time
import threading

from tkinter import* 
from picamera import PiCamera
import busio
from digitalio import DigitalInOut, Direction, Pull

import board
import adafruit_ssd1306
import queue

print("imported default Libraries")

#import DAQ.VectorNav.vectornavLib
import DAQ.ultGPS.GPS
import DAQ.PressureSensor.BMP280

while 1:
    try:  #WORK IN PROGRESS
        import DAQ.AccelerationSensor.BNO055
        o =  DAQ.AccelerationSensor.BNO055.BNO()
        print('Accel sensor successfully imported.')
    except:
        print('Error found, trying again.')
        continue

import Telemetry.RFM9X
import System.system
import Display.display2_0
import Button.button
#import Velocity.velocity

import Data.RocketConstants as rocket
import Motor.motorhat

print("imported custom Libraries")

#instatiate custom libraries classes
#v=DAQ.VectorNav.vectornavLib.vnav()
g=DAQ.ultGPS.GPS.GPS()
a=DAQ.PressureSensor.BMP280.BMP()
o=DAQ.AccelerationSensor.BNO055.BNO()
t=Telemetry.RFM9X.telemetry()
s=System.system.systemRead()
d=Display.display2_0.oled
b=Button.button.buttonOps
m=Motor.motorhat.motor()
#vel=Velocity.velocity.velocity()


#initialize threads
systemLoads = threading.Thread(target = s.systemLoads)
BMP = threading.Thread(target = a.readBMP)

#check to see if the radio is on
#d.displayFortnite()
t.radioCheck()
print("radio check succsesful")

# telemetrySend         = threading.Thread(target = t.telemetrySend,         daemon = True)
# telemetryReceive      = threading.Thread(target = t.telemetryReceive,      daemon = True)
#readVnav              = threading.Thread(target = v.readVnav,              daemon = True)#initialize again since we want to
#calculateVericalAccel = threading.Thread(target = v.calculateVericalAccel, daemon = True)

# launchsequencealt     = 
# launchsequencecoords  =
readGPS               = threading.Thread(target = g.readGPS,               daemon = True)


# Setup i2c bus  sudo i2cdetect -y 1
i2c = busio.I2C(board.SCL, board.SDA)
# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)


display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
button_a_pin = 5
button_b_pin = 6
button_c_pin = 12
canGo = True

selector = 1
scrnNum = 0
option=""


#ALRIGHT IDIOTS LISTEN UP, THIS HAS TO BE A MULTIPLE OF 3 CAUSE WE'RE TOO LAZY FOR EDGE CASES
optionList = ["1. Start Data", "2.", "3. ", "4.inch in", "5.inch out", "6.sweep", "7. ", "8. ", "9. EXIT "]

NUM_OF_SCREENS = int(len(optionList)/3)
scrnArray = [NUM_OF_SCREENS] * len(optionList)

j=0
for i in range(int(NUM_OF_SCREENS)):
    scrnArray[i] = d(optionList[j],optionList[j+1],optionList[j+2])
    j+=3

class main():
    #######################
    global q
    telemetrySendThread    = threading.Thread(target = t.telemetrySend, daemon=True)#initialize again since we want to 
    telemetryReceiveThread = threading.Thread(target = t.telemetryReceive, daemon=True)
    launchsequenceaccel   = threading.Thread(target = o.getVertAccel, daemon=True)
    t.runthread
    option=0
    q = queue.LifoQueue()
    button = threading.Thread(target = b.comm, args = (q,))
    button.start()
    #######################
    
    def killThreads():
        print('Killing all threads!')
        t.runThread(False)
        o.runThread(False)
    
    scrnArray[scrnNum].createDisplay(selector)
    def buttonA():#THIS SUBTRACTS TO COUNT WHEN PRESSED, THEN CHECKS SELECTOR AND SCRNNUM THRESHHOLDS
        global selector
        global scrnNum
        selector-=1
        
        if selector < 1:
            selector = 3
            scrnNum -= 1
            if scrnNum < 0:
                scrnNum = NUM_OF_SCREENS-1
        scrnArray[scrnNum].createDisplay(selector)
        #print(str(scrnNum) + "Selector:" + str(selector))

        
    def buttonB(): #THIS ADDS TO COUNT WHEN PRESSED, THEN CHECKS SELECTOR AND SCRNNUM THRESHHOLDS
        global selector
        global scrnNum
        selector+=1
        
        if selector > 3:
            selector = 1
            scrnNum+=1
            if scrnNum > NUM_OF_SCREENS-1:
                scrnNum = 0
        scrnArray[scrnNum].createDisplay(selector)
       # print(str(scrnNum) + "Selector:" + str(selector))
        
    def buttonC(self): #PUT CONDITIONS TO RUN FUNCTIONS FROM DISPLAY
        global selector # COMMENT OUT IF BROKEN!
        global scrnNum  # COMMENT OUT IF BROKEN!
        if scrnNum == 0 and selector == 1:
            main.killThreads()
            display.fill(0)
            display.text("send", 0, 16, 1)
            display.show()
            print('Booting up telemetry thread!')
            t.runThread(True)
              #  v.runThread(True)
               # readVnav = threading.Thread(target = v.readVnav, daemon=True)#initialize again since we want to 
              #  readVnav.start()
            self.telemetryReceiveThread.start()
            self.telemetrySendThread.start()
            # There really is no need for scrnNum 0, selector 0, as that array doesn't "exist".
        
        if scrnNum == 0 and selector == 2:
            main.killThreads()
            option="calibrate bno"
            display.fill(0)
            display.text("callibrating bno055...", 0, 16, 1)
            display.show()
        if scrnNum == 0 and selector == 3:
            main.killThreads()
            option="bno stats"
            display.fill(0)
            display.text("send", 0, 16, 1)
            display.show()
        if scrnNum == 1 and selector == 1:
            main.killThreads()
            display.fill(0)
            display.text("inching into your mom like", 0, 16, 1)
            display.show()
            m.inchin()
        if scrnNum == 1 and selector == 2:
            main.killThreads()
            display.fill(0)
            display.text("inching out of ur mom like", 0, 16, 1)
            display.show()
            m.inchout()
        if scrnNum == 1 and selector == 3:
            main.killThreads()
            option="3"
            display.fill(0)
            display.text("sweeping dem hoes like", 0, 16, 1)
            display.show()
            m.sweep()
        if scrnNum == 2 and selector == 1:
            main.killThreads()
            option="launch sequence"
            display.fill(0)
            display.text("", 0, 16, 1)
            display.show()
            print('Bootin up launch sequence thread.')
            o.runThread(True)
            self.launchsequenceaccel.start()
            
        else:
            option=""

    def detectingPresses():  # Place self if broken.
     
        while True:
#             currentQ = q.get()
#             if currentQ != None:
#                 if currentQ == "A":
#                     main.buttonA()
#                 elif currentQ == "B":
#                     main.buttonB()
#                 elif currentQ == "C":
#                     main.buttonC()
                    
            currentQ = q.get()
            if currentQ != None:
                if currentQ == "A":
                    main.buttonA()
                elif currentQ == "B":
                    main.buttonB()
                elif currentQ == "C":
                    bC = main()
                    bC.buttonC()
                    #this.buttonC()
                    
            time.sleep(.01)
    detect = threading.Thread(target = detectingPresses)
    detect.start()