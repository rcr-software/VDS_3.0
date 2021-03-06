DUBUG=0
import serial
import math
import multiprocessing
gpsData = "0,0,0"

#initialize the serial port for the GPS
gps = serial.Serial(
        port='/dev/serial0',# ttyS0/ttyAMA0 for the serial line and ttyUSB0 for the usb port
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1 
)


#gather gps data
class GPS():
    gpsTXT= open("/home/pi/Desktop/VDSv3/VDSCode/LOGS/gps_log.txt", "a")
    threadStopFlag=True
    gpsNMEAFile    = open("NMEA_Data","a")
    gpsDecimalFile = open("GPS_Decimal_Data","a")
    
    gpsAltitude    = 0
    longDec        = 0
    latDec         = 0
    
    def gpsTxtClose(self):
        self.gpsDecimalFile.close()
        self.gpsNMEAFile.close()
        
    def runThread(self,stopFlag):
        self.threadStopFlag=stopFlag
        return(stopFlag)
    
    def runProcess(self):
        self.gpsprocc = multiprocessing.Process(target = GPS.readGPS, args=(self,))
        print('GPS initialized successfully.')
        self.gpsprocc.start()
        print('GPS booted up and running properly.')
    
    def readGPS(self):
        while self.threadStopFlag:
            serialNMEA = str(gps.readline())
                    
            self.gpsTXT.write(str(gps.readline()))
            
            print(serialNMEA)
            
            gpsStateRMC = "$GPRMC" in serialNMEA
            gpsStateGGA = "$GPGGA" in serialNMEA
            
            #look for altitude in GGA
            if (gpsStateGGA == 1):
                serialNMEA  = serialNMEA.split(',')
                self.gpsAltitude = str(serialNMEA[7])
            #look for lat and long in RMC
            if (gpsStateRMC == 1):
                serialNMEA        = serialNMEA.split(',')
                latNMEA           = float( serialNMEA[3] )  
                latDirectionNMEA  = str(   serialNMEA[4] )
                longNMEA          = float( serialNMEA[5] )
                longDirectionNMEA = str(   serialNMEA[6] )
                
                #detrmine the decimal degrees direction
                if (longDirectionNMEA == "W"):
                    longDirectionDec = -1
                else:
                    longDirectionDec = 1
                    
                if (latDirectionNMEA == "N"):
                    latDirectionDec = 1
                else:
                    latDirectionDec = -1
                
                #determine the decimal degrees magnitude
                latDec  = round( latDirectionDec  * (math.floor(latNMEA  / 100) + (latNMEA  - ((math.floor(latNMEA  / 100)) * 100)) / 60), 4)   
                longDec = round( longDirectionDec * (math.floor(longNMEA / 100) + (longNMEA - ((math.floor(longNMEA / 100)) * 100)) / 60), 4)
                
                #ensure the use of trailing zeros for 4 decimal places
                temp = '{:<04}'
                self.latDec = str(temp.format(latDec))
                self.longDec = str(temp.format(longDec))
                
                #prepare the text file for google maps
                gpsData = self.longDec + "," + self.latDec + "," + self.gpsAltitude
                print(gpsData)
                
                self.gpsDecimalFile.write(gpsData)
                self.gpsNMEAFile.write(str(serialNMEA))
                self.gpsNMEAFile.write('\n')
                
    def closeGpsTxt(self):
        self.gpsTXT.close()
        return
                
            #return self.latDec, self.longDec, self.gpsAltitude
if DUBUG==True:                
    g=GPS()
    g.readGPS()