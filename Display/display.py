import adafruit_ssd1306
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import time
import subprocess
from PIL import ImageDraw
from PIL import ImageFont
from PIL import Image

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
    def displayStats(self):
        display.text('RX: ', 0, 0, 1)
        display.show()
        time.sleep(.5)
        display.fill(0) 
        display.show()
    def system_shit(self):
        while True:
            cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
            CPU = subprocess.check_output(cmd, shell = True )
            cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
            MemUsage = subprocess.check_output(cmd, shell = True )
            cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
            Disk = subprocess.check_output(cmd, shell = True )
            time.sleep(0.1)

            draw.text((x, top+8),     str(CPU), font=font, fill=255)
            draw.text((x, top+16),    str(MemUsage),  font=font, fill=255)
            draw.text((x, top+25),    str(Disk),  font=font, fill=255)

            display.image(image)
            display.show()
        time.sleep(5)
    def fuckthembitches():
        number1 = 0
        number2 = 1
        number3 = 2
        while True:
        
            daddy = ["1.We", "2.fucking" , "3.love", "4.anal", "5.bro"]
            
            if number1 == 5:
                number1 = number1-5
            if number2 == 5:
                number2 = number2-5
            if number3 == 5:
                number3 = number3-5
                
            display.text(daddy[number1], 0, 8, 1)
            display.text(daddy[number2], 0, 16, 1)
            display.text(daddy[number3], 0, 25, 1)
            
            number1 = number1 + 1
            number2 = number2 + 1
            number3 = number3 + 1
            

                
            display.show()
            
            time.sleep(1)
            
            display.fill(0)
            display.show()

# display_class = oled()
# display_class.fuckthembitches()


