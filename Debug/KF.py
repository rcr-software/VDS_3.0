test = [1,2,3]
x = len(test)
for i in range (0, x):
    print(test[i])


#############################################################################################

### Test Values
measurement = 48.54
sigma = 15 #Estimation error (Standard Deviation)
error =  5 #Measurement error (Standard Deviation)
p = (sigma ** 2) #Variance = Estimation error (Standard Deviation) squared
r = (error ** 2) #Measurement error (Standard Deviation) squared
q = 0.1 # System Process Noise
k = 0 # Global k value

### Kalman Gain
def KF_gain(measurement, sigma, error, r):
    k = (p)/(p + r) # Kalman Gain Equation
    print("Gain: {}".format(k)) #Works

    ### Estimate Current State
    x = 60 # Estimate | This could be calculated by multiplying the average velocity by the time traveled between KF calculations

    x = x + k*(measurement - x) # Estimate Current State Equation
    #print("Current State Estimate: {}".format(x)) #Works
    return sigma, p, error, r, k, x

### Update Estimate Uncertainty
def KF_update(p, k):
    p = (1 - k)*p
    #print("Current Estimate Uncertainty: {}".format(p)) #Works
    return p

### Prediction
def KF_prediction(p, q):
    p = p + q # Prediction Equation
    #print("Prediction: {}".format(p)) #Works
    return p, q

#############################################################################################

KF_gain(measurement, sigma, error, r)
print("Current State Estimate: {}".format(x)) #Works
KF_update(p, k)
print("Current Estimate Uncertainty: {}".format(p)) #Works
KF_prediction(p, q)
print("Prediction: {}".format(p)) #Works