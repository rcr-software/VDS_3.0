#%matplotlib inline
import sympy
import numpy as np
import matplotlib.pyplot as plt
from sympy.abc import x as a,y as b
import time
import serial
import numpy
import threading
import math

# Simulation function 9.8^2 = x^2 + y^2 + z^2

#Argument
x=np.linspace(-5,5,num=1000)
#Add noise
noise=np.random.rand(len(x))*2-1
#Dependent variable
y=3*x-1+noise

plt.figure(figsize=(10,10))
plt.scatter(x,y,s=1)
plt.show()
time.sleep(3)

#y=ax+b #objective function

#  e=1/2*Σ([axi+b]-yi)^2 #cost function, when the cost function is the minimum, the corresponding a and b
# 
#  Find the partial derivative of a->Σ(axi+b-yi)*xi
# 
#  Find the partial derivative of b->Σ(axi+b-yi)
# 
# e know that when the partial derivative at a and b is 0, the cost function e reaches the minimum value, so we get the binary linear equations
# 
# Σ(axi+b-yi)*xi=0
# Σ(axi+b-yi)=0
# 
#  This system of equations is about a system of binary linear equations with unknowns a and b. By solving this equation, we get a, b

result=sympy.solve([
    np.sum((a*x+b-y)*x),
    np.sum(a*x+b-y)],[a,b])
#print(result) #{x: 3.01182977621975, y: -1.00272253325765}

plt.figure(figsize=(10,10))
plt.scatter(x,y,s=1)
plt.plot(x,result[a]*x+result[b],c='red')
plt.show()
#print(type(a),type(b)) #<class 'sympy.core.symbol.Symbol'> <class 'sympy.core.symbol.Symbol'>


# Note that a and b of sympy.abc are covered here
# Set the starting point of a and b
a,b,c=0.1,0.1,0.1

#Step size, also known as learning rate
alpha=0.00001
print((a*x+b-y)*x)
#Loop over a thousand times
for i in range(1000):
    a-=alpha*np.sum((a*x+b-y)*x)
    b-=alpha*np.sum(a*x+b-y)

print(a,b) #3.0118297762197526 -1.002674927350334

plt.figure(figsize=(10,10))
plt.scatter(x,y,s=1)
plt.plot(x,a*x+b,c='black')
plt.show()

print(type(a),type(b)) #<class 'numpy.float64'> <class 'numpy.float64'>