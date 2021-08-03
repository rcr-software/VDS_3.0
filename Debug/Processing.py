import serial
from multiprocessing import Process
import time
c=" "
out=" "
class main():
    def pi():
        print ("started")
        out=" "
        while 1:
            print("Hey Baby")
            time.sleep(1)
    def man():
        while(1): 
            Abel = "god"
    if __name__ == '__main__':

        p1=Process(target=pi,args=())
        p2=Process(target=man,args=())

        p1.start() 
        p2.start()
        p1.join()
        p2.join()
# class oled2(Process):
#     def CPU(self):
#         print("started")
#         while True:
#             print("CPU")
#             display.fill(0)
#             cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
#             CPU = subprocess.check_output(cmd, shell = True )
#             time.sleep(0.5)
#             display.text(str(CPU),0,8,1)
#             cpu_temp = CPUTemperature()
#             display.text("Temperature: " + str(cpu_temp.temperature),0,16,1)
#             display.show()
# #     def display6(self):
# #         print("about to start")
# #         CPU_Process = Process(target = self.CPU)
# #         CPU_Process.start()
# #         CPU_Process.join()
# #         print("process started")
#     
#     def __init__(self):
#         Process.__init__(self)
# 
#     def run(self):
#         print("about to start")
#         CPU_Process = Process(target = self.CPU)
#         CPU_Process.start()
#         CPU_Process.join()
#         print("process started")
# 
# # if __name__ == "__main__":
# #     print("--------------The parent process starts to execute--------")
# #     print("PID of parent process: %s" % os.getpid())
# #     p1 = oled2(interval=1, name='mrsoft')
# #     p2 = oled2(interval=2)
# #     # Executing the start method on a Process class that does not help the Korean target attribute will run the run method in this class
# #     # So p1.run() will be executed here
# #     p1.start()
# #     p2.start()
# #     # Output the execution status of the processes of p1 and p2, if it is really going on, return True
# #     print("p1.is_alive=%s" % p1.is_alive())
# #     print("p2.is_alive=%s" % p2.is_alive())
# #     # Output the alias and PID of the p1 and p2 processes
# #     print("p1.name=%s" % p1.name)
# #     print("p1.pid=%s" % p1.pid)
# #     print("p2.name=%s" % p2.name)
# #     print("p2.pid=%s" % p2.pid)
# #     print("----------Waiting for the child process----------")
# #     p1.join()
# #     p2.join()
# #     print("----------- End of parent process----------")  