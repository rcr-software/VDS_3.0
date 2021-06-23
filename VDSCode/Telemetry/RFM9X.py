import adafruit_rfm9x
import board
import digitalio
from digitalio import DigitalInOut, Direction, Pull
import busio
import time
import sys

sys.path.insert(1,'/home/pi/Desktop/VDS3.0/VDSCode/ultGPS')
import GPS
sys.path.insert(1,'/home/pi/Desktop/VDS3.0/VDSCode/VectorNav')
import vectornavLib
sys.path.insert(1,'/home/pi/Desktop/VDS3.0/VDSCode/System')
import system
sys.path.insert(1,'/home/pi/Desktop/VDS3.0/VDSCode/PressureSensor')
import BMP280

# Configure RFM9x LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
prev_packet = None

g=GPS.GPS()
b=BMP280.BMP()

class telemetry():
    def telemetrySend(self):
        global packetNum
        packetNum=0
        while 1:#threadActivate ==1: 
            while 1:#sendState == 1:
                
                packetNum=packetNum+1
                
                gpsData="v, " + str(packetNum) + ',' + str(g.readGPS()[0]) + ',' + str(g.readGPS()[1]) + ',' + str(round(b.readBMP(),4)) #+ ',' + str(vertVel) + ',' + str(vertAccel) + ',' + str(yaw) + ',' + str(pitch) + ',' + str(roll) + ',' + str(CPUTemp) + ',' + str(usedRAM) + ',' + str(CPULoad) + ',' + str(gpsfix) + ',' + str(pressure) + ',' + str(battery) + ',' + str(local_rssi) + ',' + str(frequency) + ',' + str(temp1) + ',' + str(temp2) + ',' + str(temp3) + ',' + str(press1) + ',' + str(press2) + ',' + str(press3) + ',' + str(noid1) + ',' + str(noid2) + ',' + str(noid3) + ',' + str(noid4) + ',' + str(noid5) + ',' + str(noid6) + ',' + str(noid7)
                gpsPacket=bytes(gpsData,"utf-8")
                rfm9x.send(gpsPacket)
                
                #print(gpsData)
                time.sleep(.1)
                
    def telemetryReceive(self):
        while 1:#threadActivate ==1:
            while 1:#sendState == 1:
                
                global local_rssi
                packet = None
                packet = rfm9x.receive()
                    
                if packet is None:
                    print("waiting on Groundstation")
                    time.sleep(1)
                    
                else:
                    packetText = str(packet,"utf-8")
                    local_rssi=rfm9x.last_rssi()
                    
            
            time.sleep(.1)
            
    def radioCheck(self):
        try:
            rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
#             display.text('RFM9x: Detected', 0, 0, 1)
        except RuntimeError as error:
        # Thrown on version mismatch
#             display.text('RFM9x: ERROR', 0, 0, 1)
            print('RFM9x Error: ', error)
            
#         display.show()    
#         time.sleep(.5)
#         display.fill(0)
#         display.show()

