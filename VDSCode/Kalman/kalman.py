from __future__ import division
from scipy.stats import gaussian
import numpy as np

class kalman():
    def multiply(self, mu1, var1, mu2, var2):
        mean = (var1*mu2 + var2*mu1) / (var1+var2)
        variance = 1 / ((1/var1) + (1/var2))
        return (mean, variance)
    
k=kalman()

xs = np.arange(16,30,0.1)
m1, v1 = 23,5
m, v   =  k.multiply(m1,v1,m1,v1)

ys = [stats.gaussian(x,m1,v1) for x in xs]
plt.plot (xs, ys, lable='original')
ys = [stats.gaussian(x,m,v) for x in xs]
plt.plot (xs, ys, lable='multiply')