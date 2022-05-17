import multiprocessing as mp
from multiprocessing import Queue

import time

class setProcess():
    i=0
    def makeQue(self):
        self.q=Queue()
    def dosomething(self):
        while 1:
            self.i=self.i+1
            self.q.put(self.i)
            time.sleep(1)
            print("dosomething")
    def run(self):
        self.processInstant=mp.process(target=self.dosomething, args=(self,))
        self.processInstant.start()
        print("run")
    def watchdog(self):
        while 1:
            print("watchdog")
            print(self.q.get())
            time.sleep(1)
        

pro = setProcess()
pro.makeQue()
pro.run()
pro.watchdog()