import serial


class ArduinoCommunication:
    ser = ''

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        self.ser.flush()

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
        print(collected_data)
        return collected_data.split(",")

    def sendToArduino(self, sendStr):
        self.ser.flush()
        self.ser.write(("[" + str(sendStr) + "]").encode())
