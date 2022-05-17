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

class oled():
    def CPU(self):
        while True:
            display.fill(0)
            cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
            CPU = subprocess.check_output(cmd, shell = True )
            time.sleep(.01)
            display.text(str(CPU),0,8,1)
            cpu_temp = CPUTemperature()
            display.text("Temperature: " + str(cpu_temp.temperature),0,16,1)
            display.text("Exit: Hold A then C",0,25,1)
            display.show()
            btnC = DigitalInOut(board.D5)
            btnC.direction = Direction.INPUT
            btnC.pull = Pull.UP
            if not btnC.value:
                print("a pressed")
                return
    def Mem(self):
        while True:
            display.fill(0)
            cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
            MemUsage = subprocess.check_output(cmd, shell = True )
            cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
            Disk = subprocess.check_output(cmd, shell = True )
            time.sleep(0.01)
            display.text(str(MemUsage),0,8,1)
            display.text(str(Disk),0,16,1)
            display.text("Exit: Hold A then C",0,25,1)
            display.show()
            btnC = DigitalInOut(board.D5)
            btnC.direction = Direction.INPUT
            btnC.pull = Pull.UP
            if not btnC.value:
                return
    def display1(self,number_1,number_2,number_3):
        display.fill(0)
        daddy = ["1. System Check", "2. Blade Check" , "3. Sensor Check", "4. Sequences", "5. Exit"]
        display.text(daddy[number_1], 0, 8, 1)
        display.text(daddy[number_2], 0, 16, 1)
        display.text(daddy[number_3], 0, 25, 1)
        display.text("<---",100,16,1)
        display.show()
    def display2(self,arrow2):
        display.fill(0)
        daddy = ["1. CPU/Temp", "2. Mem/Disk"]
        display.text(daddy[0], 0, 8, 1)
        display.text(daddy[1], 0, 16, 1)
        display.text("<---",100,arrow2,1)
        display.show()
    def display3(self,arrow3):
        display.fill(0)
        daddy = ["1. Inch Inward", "2. Inch Outward","3. Full Sweep"]
        display.text(daddy[0], 0, 8, 1)
        display.text(daddy[1], 0, 16, 1)
        display.text(daddy[2], 0, 25, 1)
        display.text("<---",100,arrow3,1)
        display.show()      
    def display4(self,arrow4):
        display.fill(0)
        daddy = ["1. V Nav", "2. BMP280 Check", "3. GPS Check"]
        display.text(daddy[0], 0, 8, 1)
        display.text(daddy[1], 0, 16, 1)
        display.text(daddy[2], 0, 25, 1)
        display.text("<---",100,arrow4,1)
        display.show()
    def display5(self,arrow5):
        display.fill(0)
        daddy = ["1. Send Data", "2. Launch"]
        display.text(daddy[0], 0, 8, 1)
        display.text(daddy[1], 0, 16, 1)
        display.text("<---",100,arrow5,1)
        display.show()
    def display6(self):
        self.CPU()
    def display7(self):
        self.Mem()
    def display8(self):
        display.fill(0)
        display.text("Inward", 0, 8, 1)
        display.show()
    def display9(self):
        display.fill(0)
        display.text("Outward", 0, 8, 1)
        display.show()
    def display10(self):
        display.fill(0)
        display.text("Sweep", 0, 8, 1)
        display.show()
    def display11(self):
        display.fill(0)
        display.text("V Nav", 0, 8, 1)
        display.show()
    def display12(self):
        display.fill(0)
        display.text("BMP280 Check", 0, 8, 1)
        display.show()
    def display13(self):
        display.fill(0)
        display.text("GPS Check", 0, 8, 1)
        display.show()
    def display14(self):
        display.fill(0)
        display.text("Send Data Shit", 0, 8, 1)
        display.show()
    def display15(self):
        display.fill(0)
        display.text("begining launch sequence", 0, 8, 1)
        display.show()
        
    def displayLogo(self):
        time23 = .1
        image = Image.open('Zachpoo/IMG_2131.jpg').resize((display.width, display.height), Image.ANTIALIAS).convert('1')
        display.image(image)
        display.show()
        time.sleep(time23)
        image = Image.open('Zachpoo/IMG_2132.jpg').resize((display.width, display.height), Image.ANTIALIAS).convert('1')
        display.image(image)
        display.show()
        time.sleep(time23)
        image = Image.open('Zachpoo/IMG_2133.jpg').resize((display.width, display.height), Image.ANTIALIAS).convert('1')
        display.image(image)
        display.show()
        time.sleep(time23)
        image = Image.open('Zachpoo/IMG_2134.jpg').resize((display.width, display.height), Image.ANTIALIAS).convert('1')
        display.image(image)
        display.show()
        time.sleep(time23)
        image = Image.open('Zachpoo/IMG_2135.jpg').resize((display.width, display.height), Image.ANTIALIAS).convert('1')
        display.image(image)
        display.show()
        time.sleep(time23)
        image = Image.open('Zachpoo/IMG_2136.jpg').resize((display.width, display.height), Image.ANTIALIAS).convert('1')
        display.image(image)
        display.show()
        time.sleep(time23)
        image = Image.open('Zachpoo/IMG_2137.jpg').resize((display.width, display.height), Image.ANTIALIAS).convert('1')
        display.image(image)
        display.show()
        time.sleep(time23)
        image = Image.open('Zachpoo/IMG_2138.jpg').resize((display.width, display.height), Image.ANTIALIAS).convert('1')
        display.image(image)
        display.show()
        time.sleep(time23)
        image = Image.open('Zachpoo/IMG_2139.jpg').resize((display.width, display.height), Image.ANTIALIAS).convert('1')
        display.image(image)
        display.show()
        time.sleep(time23)
        image = Image.open('Zachpoo/IMG_2140.jpg').resize((display.width, display.height), Image.ANTIALIAS).convert('1')
        display.image(image)
        display.show()
        time.sleep(time23)
        image = Image.open('Zachpoo/IMG_2141.jpg').resize((display.width, display.height), Image.ANTIALIAS).convert('1')
        display.image(image)
        display.show()
        time.sleep(time23)
        image = Image.open('Zachpoo/IMG_2142.jpg').resize((display.width, display.height), Image.ANTIALIAS).convert('1')
        display.image(image)
        display.show()
        time.sleep(time23)
        image = Image.open('Zachpoo/IMG_2143.jpg').resize((display.width, display.height), Image.ANTIALIAS).convert('1')
        display.image(image)
        display.show()
        time.sleep(time23)
        image = Image.open('Zachpoo/IMG_2144.jpg').resize((display.width, display.height), Image.ANTIALIAS).convert('1')
        display.image(image)
        display.show()
        time.sleep(time23)
        image = Image.open('Zachpoo/IMG_2145.jpg').resize((display.width, display.height), Image.ANTIALIAS).convert('1')
        display.image(image)
        display.show()
        time.sleep(time23)
        image = Image.open('Zachpoo/IMG_2146.jpg').resize((display.width, display.height), Image.ANTIALIAS).convert('1')
        display.image(image)
        display.show()
        time.sleep(time23)
        image = Image.open('RCR_OLED_logo (1).jpg').resize((display.width, display.height), Image.ANTIALIAS).convert('1')
        display.image(image)
        display.show()
        time.sleep(1)
            
    def displayFortnite(self):
        display.fill(0)
        timeDelay = .05
        for x in range (1,74):
            x=str(x).zfill(3)
            location='fortnite/ezgif-frame-' + x + '.jpg'
            fortniteImg = Image.open(location).resize((display.width, display.height), Image.ANTIALIAS).convert('1')
            display.image(fortniteImg)
            display.show()
            time.sleep(timeDelay)





