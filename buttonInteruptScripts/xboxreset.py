#!/usr/bin/python

# This script will wait for a button to be pressed and then shutdown
# the Raspberry Pi.
# The button is to be connected on header 5 between pins 6 and 8.

# http://kampis-elektroecke.de/?page_id=3740
# http://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio
# https://pypi.python.org/pypi/RPi.GPIO

import RPi.GPIO as GPIO
import time
import os

# we will use the pin numbering of the SoC, so our pin numbers in the code are 
# the same as the pin numbers on the gpio headers
GPIO.setmode(GPIO.BCM)
buttonPin=22


# Pin  will be input and will have his pull up resistor activated
# so we only need to connect a button to ground
GPIO.setup(buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# ISR: if our button is pressed, we will have a falling edge on pin 23
# this will trigger this interrupt:
def Xboxreset(channel):
	# reset our Controller
	os.system("sudo pkill -f xboxdrv")
	os.system("sudo pkill -f driveRobotMapped.py")
	os.system("(sudo python /home/pi/robotarm/driveRobotMapped.py)&")


# Now we are programming pin 23 as an interrupt input
# it will react on a falling edge and call our interrupt routine "Xboxreset"
GPIO.add_event_detect(buttonPin, GPIO.FALLING)
GPIO.add_event_callback(buttonPin, Xboxreset)

# do nothing while waiting for button to be pressed
while 1:
	time.sleep(.3)
