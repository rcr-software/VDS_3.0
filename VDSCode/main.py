
#import Libraries
import time
import threading
import multiprocessing
from tkinter import* 
from picamera import PiCamera
print("imported default Libraries")

import VectorNav.vectornavLib
import ultGPS.GPS
import PressureSensor.BMP280
import Telemetry.RFM9X
import System.system
import Display.display
import Velocity.velocity
import GUI.GUI
import RocketConstants as rocket
print("imported custom Libraries")

#instatiate custom libraries classes
v=VectorNav.vectornavLib.vnav()
g=ultGPS.GPS.GPS()
b=PressureSensor.BMP280.BMP()
t=Telemetry.RFM9X.telemetry()
s=System.system.systemRead()
d=Display.display.oled()
vel=Velocity.velocity.velocity()
Gui=GUI.GUI.main()

#setup the Camera [test for cmd: raspivid -o video.h264 -t 10000]
#camera = PiCamera()
#camera.start_recording("testvid.h264")

#initialize threads
systemLoads = threading.Thread(target = s.systemLoads)
readGPS = threading.Thread(target = g.readGPS)
BMP = threading.Thread(target = b.readBMP)
#################################################
#start threads
#readVnav.start() #read vnav data
#readGPS.start()#read gps data

    
#systemLoads.start()
BMP.start()
#comm.start()
#d.displayStats()
#d.displayFortnite()
t.radioCheck() #check to see if the radio is on
print("radio check sucsesful")


i=61.52

    
print("The End") #I love Dick



v.vnavTxtClose()
def displaySelector():
    telemetrySend = threading.Thread(target = t.telemetrySend, daemon=True)
    telemetryReceive = threading.Thread(target = t.telemetryReceive, daemon=True)
    readVnav = threading.Thread(target = v.readVnav, daemon=True)#initialize again since we want to
    calculateVericalAccel = threading.Thread(target = v.calculateVericalAccel, daemon=True)
    
    telemetryStarted = False
    vnavStarted = False
    
    while 1:
        currentD = Gui.currentDisplay1()
        if currentD == 14:
            if telemetryStarted == False:
                t.runThread(True)
                
                telemetrySend = threading.Thread(target = t.telemetrySend, daemon=True)#initialize again since we want to 
                telemetryReceive = threading.Thread(target = t.telemetryReceive, daemon=True)
                telemetryReceive.start()
                telemetrySend.start()
                telemetryStarted = True
                
        elif currentD == 11:
            if vnavStarted == False:
                v.runThread(True)
                
                readVnav = threading.Thread(target = v.readVnav, daemon=True)#initialize again since we want to 
                readVnav.start()
                calculateVericalAccel = threading.Thread(target = v.calculateVericalAccel, daemon=True)#initialize again since we want to 
                calculateVericalAccel.start()
                vnavStarted = True        
        else:#if different display
            if calculateVericalAccel.is_alive():
                v.runThread(False)#terminate function
                vnavStarted = False
            if readVnav.is_alive():
                v.runThread(False)#terminate function
                vnavStarted = False
            if telemetrySend.is_alive():
                t.runThread(False)#terminate function
                telemetryStarted = False
        time.sleep(.2)

displaySelector = threading.Thread(target = displaySelector)
displaySelector.start()

#close active threads

#camera.stop_recording()

#gpsDecimalFile.close()
