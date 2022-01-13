import adafruit_ssd1306
import board
import busio

from gpiozero import CPUTemperature
from digitalio import DigitalInOut, Direction, Pull
import time

import subprocess

from PIL import ImageDraw
from PIL import ImageFont
from PIL import Image


import sys
sys.path.insert(1,'/home/pi/Desktop/VDS3.0/VDSCode/Display')
sys.path.insert(1,'/home/pi/Desktop/VDS3.0/VDSCode/Telemetry')


# Setup i2c bus  sudo i2cdetect -y 1
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)


import math
import time
import threading
import queue
import sys
sys.path.insert(1,'/home/pi/Desktop/VDS_3.0/VDSCode/Display')
sys.path.insert(1,'/home/pi/Desktop/VDS_3.0/VDSCode/Button')
import button
import display2_0

display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)

button_a_pin = 5
button_b_pin = 6
button_c_pin = 12
canGo = True

selector = 1
scrnNum = 0


#ALRIGHT IDIOTS LISTEN UP, THIS HAS TO BE A MULTIPLE OF 3 CAUSE WE'RE TOO LAZY FOR EDGE CASES
optionList = ["1. Start Data", "2.", "3. ", "4. ", "5. ", "6. ", "7. ", "8. ", "9. EXIT "]
NUM_OF_SCREENS = int(len(optionList)/3)
scrnArray = [NUM_OF_SCREENS] * len(optionList)

j=0
for i in range(int(NUM_OF_SCREENS)):
    scrnArray[i] = display2_0.oled(optionList[j],optionList[j+1],optionList[j+2])
    j+=3

class main():
    #######################
    global q
    q = queue.LifoQueue()
    button = threading.Thread(target = button.buttonOps.comm, args = (q,))
    button.start()
    #######################
    
    scrnArray[scrnNum].createDisplay(selector)
    
    def selector(self):
        return selector
    def screenNum(self):
        return scrnNum
    
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
        
    def buttonC(): #PUT CONDITIONS TO RUN FUNCTIONS FROM DISPLAY
        if scrnNum == 0 and selector == 1:
            display.fill(0)
            display.text("send", 0, 16, 1)
            display.show()
            
    def detectingPresses():
        while True:
            currentQ = q.get()
            if currentQ != None:
                if currentQ == "A":
                    main.buttonA()
                elif currentQ == "B":
                    main.buttonB()
                elif currentQ == "C":
                    main.buttonC()
            time.sleep(.01)
    detect = threading.Thread(target = detectingPresses)
    detect.start()
    
