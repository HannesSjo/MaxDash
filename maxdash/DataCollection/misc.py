import time
import threading

class MiscDataCollector:
    def __init__(self):
        # Initializing mock data
        self.msg = {
            "KMH": 0,
            "FUEL": 1.0,
            "BLINKER": (False, False) #first is left second is right
            #Might add more
        }

        self.running = threading.Event()
        self.running.set()

    def startUpdateThread(self, frequency=1.0):
        self.update_thread = threading.Thread(target=self.update, args=(frequency,))
        self.update_thread.start()

    def stopUpdateThread(self):
        self.running.clear()
        self.update_thread.join()

    def update(self, frequency=1):
        while self.running.is_set():
            self.msg["KMH"] += 1
            if (self.msg["FUEL"] - 0.001 > 0):
                self.msg["FUEL"] -= 0.001
            time.sleep(1 / frequency)

    def getData(self):
        return self.msg.copy()





