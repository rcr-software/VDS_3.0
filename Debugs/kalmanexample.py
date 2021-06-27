import numpy as np
import matplotlib.pyplot as plt



# intial parameters
n = 500
sz = (n) # size of array
t = np.linspace(0,10,n)
x = t + 2*t**2 # truth function
z = x + np.random.normal(0,7.5,size=sz) # noise

Q = 1e-4 # process variance

# allocate space for arrays
xhat=np.zeros(sz)      # a posteri estimate of x
P=np.zeros(sz)         # a posteri error estimate
xhatminus=np.zeros(sz) # a priori estimate of x
Pminus=np.zeros(sz)    # a priori error estimate
K=np.zeros(sz)         # Kalman gain

R = 0.1**2 # estimate of measurement variance


xhat[0] = 0.0
P[0] = 1.0

for i in range(1,n):

  xhatminus[i] = xhat[i-1]
  Pminus[i] = P[i-1]+Q


  K[i] = Pminus[i]/( Pminus[i]+R )
  xhat[i] = xhatminus[i]+K[i]*(z[i]-xhatminus[i])
  P[i] = (1-K[i])*Pminus[i]

plt.figure()
plt.plot(t, z,'k+',label='noisy measurements')
plt.plot(t, xhat,'b-',label='a posteri estimate')
plt.plot(t,x,color='g',label='truth value')
plt.legend()
plt.xlabel('t')
plt.ylabel('f(t)')


plt.show()