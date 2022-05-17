import math
#minimum nominal rocket values

#normal rocket values
g=9.81     # gravity
rho=1.225 # density of dry air at at 15 degrees C at sea level
cdR=.97    # drag coefficient of rocket
cdB=.97*1.35      # drag coefficient of rocket + air brakes
aR=.0022559  # cross sectional area of a rocket with 6in OD
aB=aR*1.28      # cross sectional area of a rocket with 6in OD + air brakes

dryMass = 23    # weight of the rocket
targetAlt      = 1633 # m   tagret altitude

#max nominal rocket values
maxDrymass        = 30   # kg  Rocket with no propelent mass
maxPropmass       = 10   # kg  Propleants mass
maxCdr            = 1    # _   Roeckts coefficient of drag
maxCdb            = 2    # _   Airbrakes coefficient of drag
maxAr             = 0.5  # m   Rockets cross sectional area
maxAb             = 0.5  # m   Airbrakes cross sectional area
maxAvgMotorThrust = 3000 # N   Motors average thrust
maxTargetAlt      = 1700 # m   tagret altitude
maxInterVel       = 250  # m/s current velocity
maxInterAlt       = 1700 # w   current altitude


cMin=cdR*aR*rho/2/dryMass
cMax=cdB*aB*rho/2/dryMass
Cspp =(cMin+cMax)/2

interVel = 125
interAlt = (targetAlt - math.log(math.sqrt((400*cMin*(interVel*interVel)) / 981+4) / 2) / cMin)

