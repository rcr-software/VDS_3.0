import serial

gpsData = "0,0,0"

#initialize the serial port for the GPS
gps = serial.Serial(
        port='/dev/ttyAMA0',# ttyS0/ttyAMA0 for the serial line and ttyUSB0 for the usb port
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1 
)

#gather gps data
class GPS():
    def __init__(self):
        self.gpsAltitude=0
        self.longDec=0
        self.latDec=0
        
    def readGPS(self):
        while 1:
        
            #global longDec, latDec, gpsAltitude, gpsData, y
            y = str(gps.readline())
            
            gpsStateRMC = "$GPRMC" in y
            gpsStateGGA = "$GPGGA" in y
            
            if (gpsStateGGA == 1):
                y = y.split(',')
                gpsAltitude = str(float(y[7]))
                
            if(gpsStateRMC == 1):
                gpsNMEAFile = open("NMEA_Data","a")
                gpsNMEAFile.write(y)
                gpsNMEAFile.write('\n')
                
                y = y.split(',')
                latNMEA = float(y[3])
                latDirectionNMEA = str(y[4])
                longNMEA = float (y[5])
                longDirectionNMEA = str(y[6])
                
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
                latDec = round( latDirectionDec * (math.floor(latNMEA / 100) + (latNMEA - ((math.floor(latNMEA / 100)) * 100)) / 60), 4)   
                longDec = round( longDirectionDec * (math.floor(longNMEA / 100) + (longNMEA - ((math.floor(longNMEA / 100)) * 100)) / 60), 4)
                
                #ensure the use of trailing zeros for 4 decimal places
                temp = '{:<04}'
                self.latDec = str(temp.format(latDec))
                self.longDec = str(temp.format(longDec))
                
                #prepare the text file for google maps
                gpsData = longDec + "," + latDec + "," + gpsAltitude + " "
                gpsDecimalFile = open("GPS_Decimal_Data","a")
                gpsDecimalFile.write(gpsData)
                gpsDecimalFile.close()
                gpsNMEAFile.close()
                
                print(gpsData)
                
            return self.latDec, self.longDec, self.gpsAltitude
    