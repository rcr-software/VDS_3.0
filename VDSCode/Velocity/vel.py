import math
import sympy as sym
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# from scipy.interpolate import interp1d
# from scipy.interpolate import interp2d
# from scipy.integrate import quad
# from scipy.integrate import solve_ivp




x = sym.Symbol('x')  # y = sym.Symbol('y')

SAMPLE_SIZE = 1000      # write your sample size here
POS_EQUATION = x ** 3  # write your position equation here

#Array definitions set to the size of the sample global
tArray = [0]*SAMPLE_SIZE
posArray = [0]*SAMPLE_SIZE
velArray = [0]*SAMPLE_SIZE
accelArray = [0]*SAMPLE_SIZE

M_height = 0
M_timeY = 0
M_accel = 0
M_velChange = 0
velFinal = 0
leftSide = 0
rightSide = 0

def M_velCalc(heightB, heightA, timeB, timeA):
    velAVG = (heightB - heightA)/( timeB - timeA)
    return velAVG

def curveCalc(t, eq):
    pos = eq.evalf(subs={x: t})
    velEq = sym.diff(eq)
    vel = velEq.evalf(subs={x: t})
    accelEq = sym.diff(velEq)
    accel = accelEq.evalf(subs={x: t})
    return t, pos, vel, accel

for i in range(SAMPLE_SIZE):
    tArray[i], posArray[i], velArray[i], accelArray[i] = curveCalc(i, POS_EQUATION)

    print(M_velCalc(posArray[i], posArray[i-1], tArray[i], tArray[i-1]))
    print(((M_velCalc(posArray[i], posArray[0], tArray[i], tArray[0]) / i)*4) + M_velCalc(posArray[i], posArray[i-1], tArray[i], tArray[i-1]))
    print("time: " + str(tArray[i]) + " | pos: " + str(posArray[i]) + " | Vel: " + str(velArray[i]) + " | accel: " + str(accelArray[i]))
    print('-------------')