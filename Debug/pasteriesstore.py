# Why the hell is multiprocessing so finicky?

import multiprocessing
import time

class Pasetries():
    def __init__(self, cheesecakes, eggtarts):
        self.cake_count = cheesecakes
        self.tart_count = eggtarts
        print('Store stock initialized and tracked.')
        self.cakeness = True
        self.tarts = True
    def tracker(self):
        while self.cakeness is True:
            self.cake_count -= 1
            print(f'The number of cheese cakes is {self.cake_count}.')
            time.sleep(3)
            if self.cake_count == 0:
                print('No cakes. D:')
                self.cakeness = False
    def timeless(self):
        # Keeps track of time or something.
        while self.tarts is True:
            self.tart_count += 1
            print(f'Number of tarts has been updated to {self.tart_count}.')
            time.sleep(3)
            if self.tart_count == 0:
                self.tarts = False
    def run(self):
        self.procc = multiprocessing.Process(target = Pasetries.tracker, args=(self,))
        self.tracc = multiprocessing.Process(target = Pasetries.timeless, args=(self,))
        self.procc.start()
        print('Tracker started.')
        self.tracc.start()
        print('Timeless started.')
        
    def kill(self):
        self.procc.terminate()
        print('Tracker terminated.')
        self.tracc.terminate()
        print('Timeless started.')
            

# if __name__ == '__main__':
#     store = Pasetries(15, 10)
#     store.run()