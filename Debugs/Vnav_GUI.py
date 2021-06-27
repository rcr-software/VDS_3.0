#import Libraries
import time
import serial
from tkinter import* 
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO

#setup gpio
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

#initialize the serial port
ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1 
)
#setup the Camera
#raspivid -o video.h264 -t 10000
#camera = PiCamera()
#camera.start_recording("testvid.h264")
#make a file to log data
file = open("vnav.txt","w")
#define functions
def readVnav():
    x = str(ser.readline())
    x = x.split(',')
    file.write(x[1])
    return x
        
##################################################        
#open gui 
win =Tk()
win.title("Vector Nav-100 data")
win.geometry('600x500+500+250')

def myClick():
    while 1:
        x = str(ser.readline())
        x = x.split(',')
        for i in range(0,13):
            file.write(x[i])
        file.write('\n')
        parse_txt = Label(win, text=x)
        parse_txt.pack()
    
btn_no = Button(win, text=' fuck that', command = win.destroy)
btn_yes = Button(win, text=' Yes ', command = myClick)
w = Label(win, text = 'Start parsing data?')

w.pack()
btn_no.pack(side=LEFT)
btn_yes.pack(side=RIGHT)

win.mainloop()
#end of GUI
#################################################
#read vnav data
while 1:
    if GPIO.input(10) == GPIO.HIGH:
        readVnav()
        break
        
        

#camera.stop_recording()
file.close()