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

#Pin that needs to be pulled low to shutdown
pin=25
redLightPin=14
greenLightPin=18

# we will use the pin numbering of the SoC, so our pin numbers in the code are 
# the same as the pin numbers on the gpio headers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pin  will be input and will have his pull up resistor activated
# so we only need to connect a button to ground
GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(redLightPin, GPIO.OUT)
GPIO.setup(greenLightPin, GPIO.OUT)
p=GPIO.PWM(greenLightPin, 50)

# ISR: if our button is pressed, we will have a falling edge on pin 31
# this will trigger this interrupt:
def Int_shutdown(channel):
	p.stop()
	GPIO.output(23, GPIO.LOW)
	GPIO.output(24, GPIO.LOW)
	GPIO.output(greenLightPin, GPIO.LOW)
	GPIO.output(redLightPin,GPIO.HIGH)
	# shutdown our Raspberry Pi
	os.system("sudo shutdown -h now")

# Now we are programming pin as an interrupt input
# it will react on a falling edge and call our interrupt routine "Int_shutdown"
GPIO.add_event_detect(pin, GPIO.FALLING, callback = Int_shutdown, bouncetime = 2000)
GPIO.output(redLightPin,GPIO.LOW)
p.start(0)
# do nothing while waiting for button to be pressed
while 1:
	for x in range(0,100,1):
	    p.ChangeDutyCycle(x)
	    time.sleep(.01)
	for x in range(0,100,1):
	    x=100-x
	    p.ChangeDutyCycle(x)
	    time.sleep(.01)  
