#!/usr/bin/python

#Created for NASA GSFC SSCO internship by Aaron Neely summer 2014

# This script creates a function to control the status lights on the
# RAPTOR Edge arm kits


#Pin assignments
controllerGreenPin = 23
controllerBluePin = 24
controllerRedPin = 7
bootGreenPin = 18
bootBluePin = 14
bootRedPin = 15



#GPIO setup
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(controllerGreenPin,GPIO.OUT)
GPIO.setup(controllerBluePin,GPIO.OUT)
GPIO.setup(controllerRedPin,GPIO.OUT)
GPIO.setup(bootGreenPin,GPIO.OUT)
GPIO.setup(bootBluePin,GPIO.OUT)
GPIO.setup(bootRedPin,GPIO.OUT)

#Creating the function
def status_lights(light,color,switch):
    #Check which light argument has been given
    if (light == "controller") or (light == "Controller") or (light == "CONTROLLER"):
        #Set color based on color argument
        if (color == 'blue') or (color == 'Blue') or (color == 'BLUE'):
            GPIO.output(controllerBluePin,switch)
        elif (color == 'green') or (color == 'Green') or (color == 'GREEN'):
            GPIO.output(controllerGreenPin,switch)
        elif (color == 'red') or (color == 'Red') or (color == 'RED'):
            GPIO.output(controllerRedPin,switch)
        elif (color == 'off') or (color == 'Off') or (color == 'OFF'):
            GPIO.output(controllerGreenPin,0)
            GPIO.output(controllerBluePin,0)
            GPIO.output(controllerRedPin,0)
        else:
            print "Incorrect second argument in raptorStatusLights.status_lights. Enter only 'blue' or 'green' or 'off'."        
    #Check which light argument has been given
    elif (light == "boot") or (light == "Boot") or (light == 'BOOT'):
        #Set color based on color argument
        if (color == 'blue') or (color == 'Blue') or (color == 'BLUE'):
            GPIO.output(bootBluePin,switch)
        elif (color == 'green') or (color == 'Green') or (color == 'GREEN'):
            GPIO.output(bootGreenPin,switch)
        elif (color == 'red') or (color == 'Red') or (color == 'RED'):
            GPIO.output(bootRedPin,switch)
        elif (color == 'off') or (color == 'Off') or (color == 'OFF'):
            GPIO.output(bootGreenPin,0)
            GPIO.output(bootBluePin,0)
            GPIO.output(bootRedPin,0)
        else:
            print "Incorrect second argument in raptorStatusLights.status_lights. Enter only 'blue' or 'green' or 'off'."        
    else:
        print "Incorrect first argument in raptorStatusLights.status_lights. Enter only 'controller' or 'boot'."
