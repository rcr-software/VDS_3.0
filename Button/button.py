import time
import board
from digitalio import DigitalInOut, Direction, Pull
import busio
import threading

#setup gpio
# Button A
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP
# Button B
btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP
# Button C
btnC = DigitalInOut(board.D12)
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP

class buttonOps():
    btnValA=0
    btnValB=0
    btnValC=0
    
    def comm(self):
        while 1:
            # global sendState
            # Check buttons
            if not btnA.value:
                # Button A Pressed
                sendState=1
                btnValA=1
                return btnValA
                time.sleep(1)
                
            if not btnB.value:
                # Button B Pressed
                sendState=0
                btnValB=1
                return btnValB
                time.sleep(1)
                
            if not btnC.value:
                # Button C Pressed
                btnValC=1
                return btnValC
                time.sleep(1)
                
            #print("Checking for button Press")        
            time.sleep(1)
        
            btnValA=0
            btnValB=0
            btnValC=0
        
