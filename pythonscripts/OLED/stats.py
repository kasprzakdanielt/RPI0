import subprocess
import time

import Adafruit_DHT
import Adafruit_SSD1306
import requests
from PIL import Image, ImageDraw, ImageFont

# Raspberry Pi pin configuration:
RST = None  # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

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

# Load default font.
# font = ImageFont.load_default()
# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('/home/pi/pythonscripts/OLED/VCR_OSD_MONO_1.001.ttf', 13)


def drawLCD():
	draw.rectangle((0, 0, width, height), outline=0, fill=0)
	cmd = "top -bn1 | grep load | awk '{printf \"Load: \"$(NF-2)$(NF-1)}'"
	CPU = subprocess.check_output(cmd, shell=True)
	cmd = "cat /sys/class/thermal/thermal_zone0/temp"
	cputemp = subprocess.check_output(cmd, shell=True)
	cputemp = float(cputemp) / 1000
	humidity, temperature = Adafruit_DHT.read_retry(22, 4)
	draw.text((x, top), "Temperature:" + str(round(temperature, 2)) + "*C", font=font, fill=255)
	draw.text((x, top + 13), "Humidity:" + str(round(humidity, 2)) + "%", font=font, fill=255)
	draw.text((x, top + 26), "CPUtemp:" + str(int(cputemp)) + "*C", font=font, fill=255)
	draw.text((x, top + 52), CPU.decode('utf-8'), font=font, fill=255)
	# Display image.
	disp.dim(True)
	disp.image(image)
	disp.display()


while True:
	disp.command(Adafruit_SSD1306.SSD1306_DISPLAYON)
	try:
		drawLCD()
	except:
		draw.rectangle((0, 0, width, height), outline=0, fill=0)
		drawLCD()
		pass
	time.sleep(1)
