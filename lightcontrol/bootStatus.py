#!/usr/bin/python

#Created for NASA GSFC SSCO internship by Aaron Neely summer 2014

# This script will controll the boot status light on the RAPTOR Edge arm kit
# The light will be blue while booting up and then pulse green while the kit is
# running and ready to go


import RPi.GPIO as GPIO
import time
import os

#Pins for boot status light
blueLightPin=14
greenLightPin=18

# Setup for boot status lights with GPIO library
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(blueLightPin, GPIO.OUT)
GPIO.setup(greenLightPin, GPIO.OUT)
p=GPIO.PWM(greenLightPin, 50)

# Turn off blue light and start PWM control on green light
GPIO.output(blueLightPin,GPIO.LOW)
p.start(0)
# Pulse the green light
while 1:
	for x in range(0,100,1):
	    p.ChangeDutyCycle(x)
	    time.sleep(.02)
	for x in range(0,100,1):
	    x=100-x
	    p.ChangeDutyCycle(x)
	    time.sleep(.02)  
