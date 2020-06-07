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
                line = self.ser.read_all().splitlines().pop(-2).decode('UTF-8').rstrip()
            except:
                print("error")
                self.read_serial()
            return line
