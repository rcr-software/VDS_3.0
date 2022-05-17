# libraries
import sympy
import numpy as np
import matplotlib.pyplot as plt
import time
import math

samples = 100
z = [0] * samples

# take the arbitrary path 0g to 4g
x = np.linspace(4, -1, num=samples)
# take the arbitrary path 0g to 4g
y = np.linspace(-4, 3, num=samples)
for i in range(samples):
    zSqr = (x[i] ** 2) + (y[i] ** 2) - (9.8 ** 2)
    if zSqr == abs(zSqr):
        z[i] = math.sqrt(zSqr)
    else:
        z[i] = math.sqrt(-1 * zSqr)
z = np.array(z)
# Add noise
#xNoise = np.random.rand(len(x)) * .0002 - 1
#yNoise = np.random.rand(len(y)) * .0002 - 1
#zNoise = np.random.rand(len(z)) * .0002 - 1
# add bias and gain
xGain = -1*1.6
yGain = 1.5
zGain = 1.4
xBias = 1.3
yBias = 1.2
zBias = 1.1

ix = xGain * x + xBias
iy = yGain * y + yBias
iz = zGain * z + zBias

fig = plt.figure()
ax=fig.add_subplot(111, projection='3d')
ax.scatter(x,y,z)

ax.xlabel="Actual Gravity Acceleration"
ax.ylabel="Measured Gravity Acceleration"
plt.show()
fig = plt.figure()
ax1=fig.add_subplot(111, projection='3d')
ax1.scatter(ix,iy,iz)
plt.show()

# a, b = sympy.symbols('a b')
# result=sympy.solve([
#     np.sum((a*x+b-ix)*x),
#     np.sum(a*x+b-ix)],[a,b])
# print(result)

alpha = .0001

mx,bx= 2,2
for i in range(10000):
    mx-=alpha*np.sum((mx*x+bx-ix)*x)
    bx-=alpha*np.sum(mx*x+bx-ix)
print(mx)
print(bx)