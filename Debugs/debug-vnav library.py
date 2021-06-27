from vnpy import*

s = VnSensor()
s.connect('/dev/ttyUSB3', 115200)

s.read_yaw_pitch_roll()