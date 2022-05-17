import pasteriesstore
import multiprocessing
import time

food = pasteriesstore.Pasetries(5, 10)

class Main():
    def __init__(self):
        self.qq = multiprocessing.Queue()
        # This confirms my suspicions that there shouldn't be any errors with reinitializing a process.
        # This is important because threads would throw a hissy fit anytime I restarted it.
        #self.error()
    
    def databox(self):
        food.run()
        self.qq.put(self.cake_count)
    
    def error(self):
        print('Oh no!')
if __name__ == '__main__':
    p = Main()
    p.databox()