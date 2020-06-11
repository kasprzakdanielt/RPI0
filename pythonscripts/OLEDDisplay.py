import subprocess
import threading
import time

import Adafruit_SSD1306
import ArduinioCommunication
from PIL import Image, ImageDraw, ImageFont
from pip._vendor.distlib.compat import raw_input

read_input = 0


class OLEDDisplay(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        global read_input
        RST = None  # on the PiOLED this pin isnt used

        # 128x64 display with hardware I2C:
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

        # Initialize library.
        self.disp.begin()

        # Clear display.
        self.disp.clear()
        self.disp.display()

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new('1', (self.width, self.height))

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        # Draw some shapes.
        # First define some constants to allow easy resizing of shapes.
        padding = 0
        self.top = padding
        self.bottom = self.height - padding
        # Move left to right keeping track of the current x position for drawing shapes.
        self.x = 0

        self.font = ImageFont.truetype('/home/pi/pythonscripts/misc/VCR_OSD_MONO_1.001.ttf', 13)
        self.arduinoComm = ArduinioCommunication.ArduinoCommunication()
        self.disp.command(Adafruit_SSD1306.SSD1306_DISPLAYON)

    def run(self):
        while True:
            try:
                self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
                cmd = "top -bn1 | grep load | awk '{printf \"Load: \"$(NF-2)$(NF-1)}'"
                CPU = subprocess.check_output(cmd, shell=True)
                cmd = "cat /sys/class/thermal/thermal_zone0/temp"
                cputemp = subprocess.check_output(cmd, shell=True)
                cputemp = float(cputemp) / 1000
                # draw.text((x, top), "Temperature:" + str(dhtReader.read_temperature()) + "*C", font=font, fill=255)
                self.draw.text((self.x, self.top + 13), "input:" + str(read_input), font=self.font, fill=255)
                self.draw.text((self.x, self.top + 26), "CPUtemp:" + str(int(cputemp)) + "*C", font=self.font, fill=255)
                self.draw.text((self.x, self.top + 39), "Distance:" + self.arduinoComm.read_last_distance() + "cm",
                               font=self.font, fill=255)
                self.draw.text((self.x, self.top + 52), CPU.decode('utf-8'), font=self.font, fill=255)
                # Display image.
                self.disp.dim(True)
                self.disp.image(self.image)
                self.disp.display()
            except:
                self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
            time.sleep(1)


class readInput(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global read_input
        while True:
            read_input = raw_input("Podaj cos: ")


if __name__ == '__main__':
    oled = OLEDDisplay()
    inp = readInput()
    oled.start()
    inp.start()

    oled.join()
    inp.join()
