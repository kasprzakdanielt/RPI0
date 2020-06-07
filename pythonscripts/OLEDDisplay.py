import subprocess
import time

import Adafruit_SSD1306
import ArduinioCommunication
from PIL import Image, ImageDraw, ImageFont

# from pythonscripts import DHT22

# Raspberry Pi pin configuration:

RST = None  # on the PiOLED this pin isnt used

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 0
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

font = ImageFont.truetype('/home/pi/pythonscripts/misc/VCR_OSD_MONO_1.001.ttf', 13)
# dhtReader = DHT22.Dht22(2, 2)
arduinoComm = ArduinioCommunication.ArduinoCommunication()


def drawLCD():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    cmd = "top -bn1 | grep load | awk '{printf \"Load: \"$(NF-2)$(NF-1)}'"
    CPU = subprocess.check_output(cmd, shell=True)
    cmd = "cat /sys/class/thermal/thermal_zone0/temp"
    cputemp = subprocess.check_output(cmd, shell=True)
    cputemp = float(cputemp) / 1000
    # draw.text((x, top), "Temperature:" + str(dhtReader.read_temperature()) + "*C", font=font, fill=255)
    # draw.text((x, top + 13), "Humidity:" + str(dhtReader.read_humidity()) + "%", font=font, fill=255)
    draw.text((x, top + 26), "CPUtemp:" + str(int(cputemp)) + "*C", font=font, fill=255)
    draw.text((x, top + 39), "Distance:" + arduinoComm.read_serial(), font=font, fill=255)
    draw.text((x, top + 52), CPU.decode('utf-8'), font=font, fill=255)
    # Display image.
    disp.dim(True)
    disp.image(image)
    disp.display()


disp.command(Adafruit_SSD1306.SSD1306_DISPLAYON)
while True:
    try:
        drawLCD()
    except:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
    time.sleep(1)
