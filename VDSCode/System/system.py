import os
import subprocess
import time

class systemRead:
    def systemLoads(self):
        while 1:
            global CPUTemp, CPULoad, RAM
            #Tempurature of the Raspbery Pi CPU
            CPUTemp = os.popen("vcgencmd measure_temp").readline()
            CPUTemp = CPUTemp.replace('temp=','')
            CPUTemp = CPUTemp.replace('\n','')
           #Determines the % load on the CPU
            cmd = "top -bn1 | grep load | awk '{printf \"%.1f\", $(NF-2)}'"
            CPULoad = str(10*float(subprocess.check_output(cmd, shell = True )))
            
            # Return RAM information (unit=kb) in a list                                        
            # Index 0: total RAM                                                                
            # Index 1: used RAM                                                                 
            # Index 2: free RAM  
            p = os.popen('free')
            for i in (0,1,2):
                line = p.readline()
                if i==2:
                    RAM = line.split()[1:4]
                    usedRam = RAM[1]
            #print(CPUTemp)
            time.sleep(1) 
