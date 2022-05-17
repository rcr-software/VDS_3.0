DEBUG=0#use this to test if module works

import adafruit_rfm9x
import board
from digitalio import DigitalInOut
import busio
import time
import sys
import multiprocessing

sys.path.insert(1,'/home/pi/Desktop/VDSv3/VDSCode/DAQ/ultGPS')
import GPS
sys.path.insert(1,'/home/pi/Desktop/VDSv3/VDSCode/DAQ/VectorNav')
#import vectornavLib
sys.path.insert(1,'/home/pi/Desktop/VDSv3/VDSCode/System')
import system
sys.path.insert(1,'/home/pi/Desktop/VDSv3/VDSCode/DAQ/PressureSensor')
import BMP280

# Configure RFM9x LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
rfm9x.enable_crc = True
prev_packet = None

g=GPS.GPS()
b=BMP280.BMP()
#v=vectornavLib.vnav()
debug = 0

class telemetry():
    threadStopFlag=True
    global Ready, time1, packetNum
    packetNum = 0
    Ready = False
    time1 = 0
    
    def runProcess(self):
        self.tsend = multiprocessing.Process(target = telemetry.telemetrySend, args=(self,))
        self.treceive = multiprocessing.Process(target = telemetry.telemetryReceive, args=(self,))
        self.tsend.start()
        self.treceive.start()
        print('Processes successfully initialized and started.')
        
    def killProcess(self):
        self.tsend.terminate()
        self.treceive.terminate()
        print('Processes killed.')
    
    def telemetrySend(self):
        global packetNum, Ready
        packetNum=0
        print('Telemetry send is now up and going!')
                    
    def telemetryReceive(self):
        global Ready, time1,packetNum
        try:
            rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
            print("RADIO WORKS")
        except RuntimeError as error:
            display.text('RFM9x: ERROR', 0, 0, 1)
            if debug:
                print('RFM9x Error: ', error)
                
        while not Ready and self.threadStopFlag:#threadActivate ==1:     str(g.readGPS()[0]) + ',' + str(g.readGPS()[1]) + ',' +   
            global local_rssi
            packet = None
            packet = rfm9x.receive()
                
            if packet is None:
                print("waiting on Groundstation then will start sending Data; Time: " + str(time1))
                time1 = time1 + 1
                
            else:
                try:
                    packetText = str(packet,"utf-8")
                    if packetText == "Ready":
                        print("Initial Packet Received, SENDING DATA")
                        Ready = True
                except:
                    if debug:
                        print("Terrible Packet Quality Received")
        
        while Ready and self.threadStopFlag:
            
            packet = rfm9x.receive()
            print(rfm9x.receive())
            packetNum=packetNum+1
            gpsData="v:" + str(format(packetNum,'08d')) + ',' +  str(format(round(b.readBMP(),4), '08f')) + ',' + str(format(rfm9x.last_rssi,'04d'))# + ',' + str(v.yaw) + ',' + str(v.pitch) + ',' + str(v.roll)# + ',' + str(CPUTemp) + ',' + str(usedRAM) + ',' + str(CPULoad) + ',' + str(gpsfix) + ',' + str(pressure) + ',' + str(battery) + ',' + str(local_rssi) + ',' + str(frequency) + ',' + str(temp1) + ',' + str(temp2) + ',' + str(temp3) + ',' + str(press1) + ',' + str(press2) + ',' + str(press3) + ',' + str(noid1) + ',' + str(noid2) + ',' + str(noid3) + ',' + str(noid4) + ',' + str(noid5) + ',' + str(noid6) + ',' + str(noid7)
            gpsPacket=bytes(gpsData,"utf-8")
            rfm9x.send(gpsPacket)
            if debug:
                print(gpsData)
            time.sleep(.1)  #how many packets a second?                 
                           
    def radioCheck(self):
        try:
            rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
        except RuntimeError as error:
            display.text('RFM9x: ERROR', 0, 0, 1)
            if debug:
                print('RFM9x Error: ', error)
                                 
    
if DEBUG==1:
    r=telemetry()
    r.radioCheck()
    r.telemetryReceive()
    
if __name__ == '__main__':
    t = telemetry()
    t.runProcess()
