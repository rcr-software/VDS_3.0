import sympy as sys

global I, prevError, time
prevError = 0
I = 0
pGain = 1
iGain = 2
dGain = 3
x = sys.Symbol("x")
time = 0

def PID(error,deltaTime):
    
    global I,prevError, time
    time = time + deltaTime
    P = error * pGain
    I = I + error*deltaTime
    D = (error-prevError)/deltaTime * dGain
    
    final = P + I + D
    
    prevError = final
    return final

def main():
    
    #print(PID(error,deltaTime))
    print("Current PID Error: " + str(PID(2.500,2.500)))
main()    

