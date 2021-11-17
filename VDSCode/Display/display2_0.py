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
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
display.fill(0)
display.show()
width = display.width
height = display.height
x = 0
padding = -2
top = padding
bottom = height - padding

image = Image.new('1',(width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

#IGNORE EVERYTHING ABOVE THIS FUTURE PLEBIANS -briar s

#in this here class below, add your functions that you wish to call in the gui EX CPU and MEM

class oled:
    
    def __init__(self, task1, task2, task3): #THIS INITIALIZES
        self.task1 = task1#DONT TOUCH UNLESS YOU KNOW WHAT YOUR DOIN
        self.task2 = task2
        self.task3 = task3

    def createDisplay(self, icount): #THIS CREATES A SCENE ON THE OLED THAT YOU CAN SEE. WITH LIKE YOUR EYES AND STUFF
        #DONT TOUCH THIS YOU NERD
        display.fill(0)
        display.text(self.task1, 0, 8, 1)
        display.text(self.task2, 0, 16, 1)
        display.text(self.task3, 0, 25, 1)
        
        if icount == 1:  
            display.text("<---",100,8,1)
        elif icount == 2:#EACH OF THESE CONDITIONS DETERMINES WHERE THE ARROW POINTS BASED ON THE COUNTER
            display.text("<---",100,16,1)
        elif icount == 3:
            display.text("<---",100,25,1)
        display.show()
        
    def CPU(self): #EXAMPLE FUNCTION TO BE CALLED
        while True: #TOUCH THIS
            display.fill(0)
            cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
            CPU = subprocess.check_output(cmd, shell = True )
            time.sleep(.01)
            display.text(str(CPU),0,8,1)
            cpu_temp = CPUTemperature()
            display.text("Temperature: " + str(cpu_temp.temperature),0,16,1)
            display.text("Exit: Press A",0,25,1)
            display.show()
            btnC = DigitalInOut(board.D5)
            btnC.direction = Direction.INPUT
            btnC.pull = Pull.UP
            if not btnC.value:
                print("a pressed")
                return
            
    def Mem(self):#EXAMPLE FUNCTION TO BE CALLED
        while True:#TOUCH THIS
            display.fill(0)
            cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
            MemUsage = subprocess.check_output(cmd, shell = True )
            cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
            Disk = subprocess.check_output(cmd, shell = True )
            time.sleep(0.01)
            display.text(str(MemUsage),0,8,1)
            display.text(str(Disk),0,16,1)
            display.text("Exit: Press A",0,25,1)
            display.show()
            btnC = DigitalInOut(board.D5)
            btnC.direction = Direction.INPUT
            btnC.pull = Pull.UP
            if not btnC.value:
                return