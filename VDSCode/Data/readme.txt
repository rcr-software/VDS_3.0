here are some varibale names you will probably use
1.Instalation of basic tools:

  1.1 update raspberry pi
    sudo apt full-upgrade
    sudo apt-get install python3-pip

  1.2 libraries
    pip3 install adafruit-circuitpython-ssd1306
    apt-get install python3-pil

    pip3 install matplotlib
    pip3 install numpy

    pip3 install adafruit-circuitpython-bmp280 

    pip3 install adafruit-circuitpython-rfm9x
    pip3 install sympy
    sudo apt-get install python3-gi-cairo
    sudo apt-get install python-gobject-cairo



2.RaspberryPi configuration
  2.1 interfaces
    sudo raspi-config
    go to interface options
    select all options

3. github
  3.1 configuration
    go to the directory you want to push to RCR's repo using ls and cd
    git init
    git config --global user.email "your email"
    git config --global user.name "your name"
  3.2 pushing to repo
    git commit -m "what you are commiting"
    git push
      follow directions you nub




longDec=38.2527                      
latDec=85.7585                       
bmp280Alt=0
vertAccel=0
yaw=0
pitch=0
roll=0
CPUTemp=0
CPULoad=0
usedRAM = 0
gpsfix=0
pressure=0
battery=0
local_rssi=0
frequency=915                         
temp1=0
temp2=0
temp3=0
press1=0
press2=0
press3=0
noid1=0
noid2=0
noid3=0
noid4=0
noid5=0
noid6=0
noid7=0