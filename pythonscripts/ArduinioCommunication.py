import re

import serial


class ArduinoCommunication:
    ser = ''

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.ser.flush()

    def read_serial(self):
        self.ser.flush()
        if self.ser.in_waiting > 0:
            line = "-"
            try:
                line = self.ser.read_all().splitlines()
            except:
                print("error")
            return line

    def read_last_distance(self):
        stack = self.read_serial()
        pop = 0
        while not stack.pop(pop).decode("UTF-8").startswith("Distance:"):
            pop = pop - 1
        return re.match(r'Distance: (?P<distance>\d*)', stack.pop(pop).decode("UTF-8")).group("distance")
