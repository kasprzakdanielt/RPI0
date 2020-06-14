import threading
import time

import serial


class ArduinoCommunication(threading.Thread):
    ser = ''
    sendStrold = ""

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        time.sleep(3)
        self.ser.flush()
        self.queue = queue
        print("ArduinoCommunication has been initialized")

    def read_serial(self):
        x = b'd'
        collected_data = ""
        if self.ser.in_waiting > 0:
            while x.decode() != "<":
                x = self.ser.read()
            x = self.ser.read()
            while x.decode() != ">":
                collected_data = collected_data + x.decode()
                x = self.ser.read()
        return collected_data.split(",")

    def run(self):
        while True:
            if not self.queue.empty():
                send_str = self.queue.get_nowait()
                if self.sendStrold != send_str:
                    self.ser.write(str.encode("[" + str(send_str) + "]"))
                    self.ser.flush()
                    self.sendStrold = send_str
                    self.queue.task_done()
