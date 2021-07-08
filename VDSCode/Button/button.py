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
        btnA1 = True
        btnB1 = True
        btnC1 = True
        while 1:
            # global sendState
            # Check buttons
            if not btnA.value:
                # Button A Pressed
                if btnA1:
                    print("A")
                    btnValA=1
                    btnA1 = False 
            if btnA.value:
                btnA1 = True
                
            if not btnB.value:
                # Button B Pressed
                if btnB1:
                    print("B")
                    btnValB=1
                    btnB1 = False
            if btnB.value:
                btnB1 = True
                
            if not btnC.value:
                # Button C Pressed
                if btnC1:
                    print("C")
                    btnValC=1
                    btnC1 = False
            if btnC.value:
                btnC1 = True
                
            btnValA=0
            btnValB=0
            btnValC=0
            time.sleep(.01)
            
#dc1.displayLogo()
#dc1.fuckthembitches()

#t = dc1.number2_2
#print(t)
