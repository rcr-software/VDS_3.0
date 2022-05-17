#minimum nominal rocket values
minC = 1
#normal rocket values
g=9.81     # gravity
rho=1.18 # density of dry air at at 15 degrees C at sea level
cd=.85    # coefficient of drag
a=.0022559  # cross sectional area of a rocket with 6in OD
m = 1.4345    # weight of the rocket
TargetAlt      = 1700 # m   tagret altitude

c=(.5*rho*cd*a)/m
print(c)

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