import time
import sys
import threading
import RPi.GPIO as GPIO
import board

sys.path.insert(1,'/home/pi/Desktop/VDS_3.0/VDSCode/Display')
sys.path.insert(1,'/home/pi/Desktop/VDS_3.0/VDSCode/Button')
import button
import display
button_a_pin = 5
button_b_pin = 6
button_c_pin = 12
import queue
dc1 = display.oled()
num1 = 0
num2 = 1
num3 = 2
arrow2 = 9
arrow3 = 8
arrow4 = 8
arrow5 = 8
canGo = True
global currentDisplay
currentDisplay = 1

d=display.oled()
#d.displayFortnite()
d.displayLogo()
class main():
    global q
    q = queue.LifoQueue()
    button = threading.Thread(target = button.buttonOps.comm, args = (q,))
    button.start()
    global currentDisplay
    #dc1.displayLogo()
    global num1,num2,num3,arrow2
    dc1.display1(num1,num2,num3)
    def currentDisplay1(self):
        return currentDisplay
    def buttonA():
        global num1,num2,num3,arrow2,arrow3,arrow4,arrow5,currentDisplay
        if currentDisplay == 1:
            num1 = num1 - 1
            num2 = num2 - 1
            num3 = num3 - 1

            if num1 == -1:
                num1 = num1+5
            if num2 == -1:
                num2 = num2+5
            if num3 == -1:
                num3 = num3+5

            dc1.display1(num1,num2,num3)
        elif currentDisplay == 2:
            if arrow2 == 9:
                arrow2 = 17
            else:
                arrow2 = 9
            dc1.display2(arrow2)
        elif currentDisplay == 3:
            arrow3 = arrow3 + 8
            if arrow3 == 32:
                arrow3 = 8
            dc1.display3(arrow3)
        elif currentDisplay == 4:
            arrow4 = arrow4 + 8
            if arrow4 == 32:
                arrow4 = 8
            dc1.display4(arrow4)
        elif currentDisplay == 5:
            arrow5 = arrow5 + 8
            if arrow5 == 32:
                arrow5 = 8
            dc1.display5(arrow5)

    def buttonB():
        global num1,num2,num3,arrow2,arrow3,arrow4,arrow5,currentDisplay
        if currentDisplay == 1:
            num1 = num1 + 1
            num2 = num2 + 1
            num3 = num3 + 1

            if num1 == 5:
                num1 = num1-5
            if num2 == 5:
                num2 = num2-5
            if num3 == 5:
                num3 = num3-5

            dc1.display1(num1,num2,num3)
        elif currentDisplay == 2:
            if arrow2 == 9:
                arrow2 = 17
            else:
                arrow2 = 9
            dc1.display2(arrow2)
        elif currentDisplay == 3:
            arrow3 = arrow3 - 8
            if arrow3 == 0:
                arrow3 = 24
            dc1.display3(arrow3)
        elif currentDisplay == 4:
            arrow4 = arrow4 - 8
            if arrow4 == 0:
                arrow4 = 24
            dc1.display4(arrow4)
        elif currentDisplay == 5:
            arrow5 = arrow5 - 8
            if arrow5 == 0:
                arrow5 = 24
            dc1.display5(arrow5)
    def buttonC():
        global num2,arrow2,currentDisplay,arrow3,arrow4,arrow5
        if currentDisplay == 1:
            if num2 == 0:
                dc1.display2(arrow2)
                currentDisplay = 2
            elif num2 == 1:
                dc1.display3(arrow3)
                currentDisplay = 3
            elif num2 == 2:
                dc1.display4(arrow4)
                currentDisplay = 4
            elif num2 == 3:
                dc1.display5(arrow5)
                currentDisplay = 5
            elif num2 == 4:
                currentDisplay = 16
                
        elif currentDisplay == 2:
            if arrow2 == 9:
                dc1.display6()
                currentDisplay = 6
            else:
                dc1.display7()
                currentDisplay = 7
        elif currentDisplay == 3:
            if arrow3 == 8:
                dc1.display8()
                currentDisplay = 8
            elif arrow3 == 16:
                dc1.display9()
                currentDisplay = 9
            else:
                dc1.display10()
                currentDisplay = 10
        elif currentDisplay == 4:
            if arrow4 == 8:
                dc1.display11()
                currentDisplay = 11
            elif arrow4 == 16:
                dc1.display12()
                currentDisplay = 12
            else:
                dc1.display13()
                currentDisplay = 13
        elif currentDisplay == 5:
            if arrow5 == 8:
                dc1.display14()
                currentDisplay = 14
            elif arrow5 == 16:
                dc1.display15()
                currentDisplay = 15
        elif currentDisplay == 6:
            dc1.display1(num1,num2,num3)  
            currentDisplay = 1
        elif currentDisplay == 7:
            dc1.display1(num1,num2,num3)
            currentDisplay = 1
        else:
            dc1.display1(num1,num2,num3)
            currentDisplay = 1
            
    def detectingPresses():
        global currentDisplay
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
