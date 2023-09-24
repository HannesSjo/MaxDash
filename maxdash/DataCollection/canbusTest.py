import time
import threading

class CanBusDataCollector:
    def __init__(self):
        # Initializing mock data
        self.msg = {
            "RPM": 1000,
            "TPS": 0.0, # TEXT #4
            "MAP": -80.0, # TEXT #1
            "AFR": 14.7, # Mätare
            "BT": 22.0, # NO
            "V": 13.50, # TEXT #2
            "IAT": 22.0, # TEXT #3
            "CT": 80.0, # Mätare
            "ERR": 0, # VarningsLampa
            "OilP": 100.0, # Mätare 
            "OilT": 90.0  # Mätare
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
            self.msg["RPM"] += 1
            self.msg["TPS"] += 0.001
            self.msg["V"] -= 0.001
            self.msg["IAT"] += 0.001
            self.msg["CT"] += 1
            self.msg["MAP"] += 0.01
            time.sleep(1 / frequency)

    def getData(self):
        return self.msg.copy()





