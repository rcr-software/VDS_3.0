# VDS_3.0
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


Start-up main.py on reboot:
In order to start up a script on raspberry pi, you must create a service that executes the script. Ordinarily, you'd use rc.local or ecron but both of those do not function on the current raspberry pi due to unknown issues. In order to create a service use the following template:

sudo nano /etc/systemd/system/service-name-here.service
[Unit]
Description= description-here Service
After=multi-user.target

[Service]
Type=idle
User=pi
ExecStart=/usr/bin/python3 file-directory-here
WorkingDirectory=/home/pi

Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target![image](https://user-images.githubusercontent.com/94311067/161160006-214f1e1b-8aaf-48a7-ac6d-89c2a65d28bc.png)
