
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
import Display.display2_0
import Velocity.velocity
import GUI.gui2_0
import RocketConstants as rocket
print("imported custom Libraries")

#instatiate custom libraries classes
v=VectorNav.vectornavLib.vnav()
g=ultGPS.GPS.GPS()
b=PressureSensor.BMP280.BMP()
t=Telemetry.RFM9X.telemetry()
s=System.system.systemRead()
vel=Velocity.velocity.velocity()
Gui=GUI.gui2_0.main()



#initialize threads
systemLoads = threading.Thread(target = s.systemLoads)

BMP = threading.Thread(target = b.readBMP)
#################################################

#d.displayFortnite()
t.radioCheck() #check to see if the radio is on
print("radio check succsesful")

def displaySelector():
    telemetrySend         = threading.Thread(target = t.telemetrySend,         daemon = True)
    telemetryReceive      = threading.Thread(target = t.telemetryReceive,      daemon = True)
    readVnav              = threading.Thread(target = v.readVnav,              daemon = True)#initialize again since we want to
    calculateVericalAccel = threading.Thread(target = v.calculateVericalAccel, daemon = True)
    readGPS               = threading.Thread(target = g.readGPS,               daemon = True)
    
    telemetryStarted = False
    vnavStarted      = False
    cpuStarted       = False
    memStarted       = False
    inwardStarted    = False
    outwardStarted   = False
    sweepStarted     = False
    bm8280Started    = False
    gpsStarted       = False


    while 1:
        screenNum = Gui.screenNum()
        selector = Gui.selector()
        if screenNum == 0 and selector == 1: #data send
            if telemetryStarted == False:
                t.runThread(True)
                v.runThread(True)
                #g.runThread(True)
                #b.runThread(True)
 
                #readBMP = threading.Thread(target = b.readBMP, daemon=True)#initialize again since we want to 
                #readBMP.start()
                
                readVnav = threading.Thread(target = v.readVnav, daemon=True)#initialize again since we want to 
                readVnav.start()
                
                #readGPS = threading.Thread(target = g.readGPS, daemon=True)#initialize again since we want to 
                #readGPS.start()


                
                telemetrySend    = threading.Thread(target = t.telemetrySend, daemon=True)#initialize again since we want to 
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
                
                v.gradientDecent()
                vnavStarted = True
               
                
#         elif currentD == 6: #CPU/Temp
#             
#             if cpuStarted == False:
#                 something.runThread(True)
#                 something = threading.Thread(target = something, daemon=True)
#                 cpuStarted = True
#                 
#         elif currentD == 7: #Memory/Disk
#             
#             if memStarted == False:
#                 something.runThread(True)
#                 something = threading.Thread(target = something, daemon=True)
#                 memStarted = True
#                 
#         elif currentD == 8: #Inward Inch
#             
#             if inwardStarted == False:
#                 something.runThread(True)
#                 something = threading.Thread(target = something, daemon=True)
#                 inwardStarted = True
#                 
#         elif currentD == 9: #Outward Inch
#             
#             if outwardStarted == False:
#                 something.runThread(True)
#                 something = threading.Thread(target = something, daemon=True)
#                 outwardStarted = True
#                 
#         elif currentD == 10: #Full Sweep
#             
#             if sweepStarted == False:
#                 something.runThread(True)
#                 something = threading.Thread(target = something, daemon=True)
#                 sweepStarted = True
#                 
#         elif currentD == 12: #BM8280 Check
#             
#             if bm8280Started == False:
#                 something.runThread(True)
#                 something = threading.Thread(target = something, daemon=True)
#                 bm8280Started = True
#                 
        elif currentD == 13: #GPS Check
            if gpsStarted == False:
                g.runThread(True)
                
                readGPS = threading.Thread(target = g.readGPS, daemon=True)#initialize again since we want to 
                readGPS.start()

                gpsStarted = True
                
        elif currentD == 15: #main launch sequence
            #setup the Camera [test for cmd: raspivid -o video.h264 -t 10000]
            #camera = PiCamera()
            #camera.start_recording("testvid.h264")
            print("screen 15")
        elif currentD == 16: #main launch sequence
            print("Exit")
            #camera.stop_recording()
            b.close()
            v.closeVnavText()
            g.close()
            gpsDecimalFile.close()
            
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
#             if something.is_alive():
#                 something.runThread(False)
#                 cpuStarted = False
#             if something.is_alive():
#                 something.runThread(False)
#                 memStarted = False
#             if something.is_alive():
#                 something.runThread(False)
#                 inwardStarted = False
#             if something.is_alive():
#                 something.runThread(False)
#                 outwardStarted = False
#             if something.is_alive():
#                 something.runThread(False)
#                 sweepStarted = False
#             if something.is_alive():
#                 something.runThread(False)
#                 bm8280Started = False
            if readGPS.is_alive():
                g.runThread(False)
                gpsStarted = False


        time.sleep(.2)

displaySelector = threading.Thread(target = displaySelector)
displaySelector.start()

#close active threads