import math
import time
import threading
import queue
import sys
sys.path.insert(1,'/home/pi/Desktop/VDS_3.0/VDSCode/Display')
sys.path.insert(1,'/home/pi/Desktop/VDS_3.0/VDSCode/Button')
import button
import display2_0

button_a_pin = 5
button_b_pin = 6
button_c_pin = 12
canGo = True

selector = 1
scrnNum = 0


#ALRIGHT IDIOTS LISTEN UP, THIS HAS TO BE A MULTIPLE OF 3 CAUSE WE'RE TOO LAZY FOR EDGE CASES
optionList = ["1. ", "2. ", "3. ", "4, ", "5. ", "6. ", "7. ", "8 ", "9 "]
NUM_OF_SCREENS = int(len(optionList)/3)
scrnArray = [NUM_OF_SCREENS] * len(optionList)

j=0
for i in range(int(NUM_OF_SCREENS)):
    scrnArray[i] = display2_0.oled(optionList[j],optionList[j+1],optionList[j+2])
    j+=3

class main():
    #######################
    global q
    q = queue.LifoQueue()
    button = threading.Thread(target = button.buttonOps.comm, args = (q,))
    button.start()
    #######################
    
    scrnArray[scrnNum].createDisplay(selector)
    
    def buttonA():#THIS SUBTRACTS TO COUNT WHEN PRESSED, THEN CHECKS SELECTOR AND SCRNNUM THRESHHOLDS
        global selector
        global scrnNum
        selector-=1
        
        if selector < 1:
            selector = 3
            scrnNum -= 1
            if scrnNum < 0:
                scrnNum = NUM_OF_SCREENS-1
        scrnArray[scrnNum].createDisplay(selector)
        
        
    def buttonB(): #THIS ADDS TO COUNT WHEN PRESSED, THEN CHECKS SELECTOR AND SCRNNUM THRESHHOLDS
        global selector
        global scrnNum
        selector+=1
        
        if selector > 3:
            selector = 1
            scrnNum+=1
            if scrnNum > NUM_OF_SCREENS-1:
                scrnNum = 0
        scrnArray[scrnNum].createDisplay(selector)
        
    def buttonC(): #PUT CONDITIONS TO RUN FUNCTIONS FROM DISPLAY
        if scrnNum == 0 and selector == 1:
            scrnArray[scrnNum].CPU()
            
    def detectingPresses():
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