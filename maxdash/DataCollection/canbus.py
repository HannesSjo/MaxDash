import os
import can
import time
import threading

class CanBusDataCollector:
    def __init__(self):
        self.msg = {
            "RPM": None, "TPS": None, "MAP": None, "AFR": None, "BT": None, 
            "V": None, "IAT": None, "CT": None, "ERR": None, 
            "OilP": None, "OilT": None
        }

        os.system('sudo ip link set can0 type can bitrate 500000')
        os.system('sudo ifconfig can0 up')
        self.can0 = can.interface.Bus(channel='can0', bustype='socketcan')

    def startUpdateThread(self, frequency=1.0):
        self.update_thread = threading.Thread(target=self.update, args=(frequency,))
        self.update_thread.start()



    def update(self, frequency=1.0):
        ids = [0x520, 0x530, 0x534, 0x536, 0x537]
        sleep_duration = (1 / (60 * frequency)) if frequency != 0 else 0
        can_id_map = {
            0x520: self.process_0x520,
            0x537: self.process_0x537,
            0x530: self.process_0x530,
            0x534: self.process_0x534,
            0x536: self.process_0x536
        }

        for can_id in ids:
            self.can0.set_filters([{"can_id": can_id, "can_mask": 0xFFFFFF}])
            res = self.can0.recv(10.0)
            if res:
                can_id_map.get(res.arbitration_id, lambda x: None)(res.data)
            time.sleep(sleep_duration)

    def process_0x520(self, data):
        self.msg["RPM"] = self.formatter(data[0], data[1])
        self.msg["TPS"] = self.formatter(data[2], data[3]) * 0.1
        self.msg["MAP"] = self.formatter(data[4], data[5]) * 0.1
        self.msg["AFR"] = (self.formatter(data[6], data[7]) * 0.001) * 14.7

    def process_0x537(self, data):
        self.msg["BT"] = self.formatter(data[6], data[7]) * 0.1

    def process_0x530(self, data):
        self.msg["V"] = self.formatter(data[0], data[1]) * 0.01
        self.msg["IAT"] = self.formatter(data[4], data[5]) * 0.1
        self.msg["CT"] = self.formatter(data[6], data[7]) * 0.1

    def process_0x534(self, data):
        self.msg["ERR"] = self.formatter(data[4], data[5])

    def process_0x536(self, data):
        self.msg["OilP"] = self.formatter(data[4], data[5]) * 0.1
        self.msg["OilT"] = self.formatter(data[6], data[7]) * 0.1

    @staticmethod
    def formatter(pos0, pos1):
        combined = (pos1 << 8) | pos0
        return combined

    def getData(self):
        return self.msg