import time
import sys
import threading
sys.path.insert(1,'/home/pi/Desktop/VDS3.0/VDSCode/Display')
sys.path.insert(1,'/home/pi/Desktop/VDS3.0/VDSCode/Button')
import display
import button as btn


dc1 = display.oled()
bc1 = btn.buttonOps()
#This is the start display, will be turned on
#dc1.displayLogo()

menu = threading.Thread(target = dc1.fuckthembitches)
#menu.start()
buttonDetect = threading.Thread(target = bc1.comm)
buttonDetect.start()
def changed():
    print("1st button")
class eatyourbreakfast():
    def button1():
        print("1st button")

dc1.displayFortnite()
dc1.displayLogo()



