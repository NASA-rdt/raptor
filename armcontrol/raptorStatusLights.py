#!/usr/bin/python


#Pin assignments
controllerGreenPin = 23
controllerBluePin = 24
bootGreenPin = 18
bootBluePin = 14



#GPIO setup
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(controllerGreenPin,GPIO.OUT)
GPIO.setup(controllerBluePin,GPIO.OUT)
GPIO.setup(bootGreenPin,GPIO.OUT)
GPIO.setup(bootBluePin,GPIO.OUT)


def status_lights(light,color):
    if (light == "controller") or (light == "Controller") or (light == "CONTROLLER"):
        if (color == 'blue') or (color == 'Blue') or (color == 'BLUE'):
            GPIO.output(controllerBluePin,1)
            GPIO.output(controllerGreenPin,0)
        elif (color == 'green') or (color == 'Green') or (color == 'GREEN'):
            GPIO.output(controllerGreenPin,1)
            GPIO.output(controllerBluePin,0)
        elif (color == 'off') or (color == 'Off') or (color == 'OFF'):
            GPIO.output(controllerGreenPin,0)
            GPIO.output(controllerBluePin,0)
        else:
            print "Incorrect second argument in raptorStatusLights.status_lights. Enter only 'blue' or 'green' or 'off'."        
    elif (light == "boot") or (light == "Boot") or (light == 'BOOT'):
        if (color == 'blue') or (color == 'Blue') or (color == 'BLUE'):
            GPIO.output(bootBluePin,1)
            GPIO.output(bootGreenPin,0)
        elif (color == 'green') or (color == 'Green') or (color == 'GREEN'):
            GPIO.output(bootGreenPin,1)
            GPIO.output(bootBluePin,0)
        elif (color == 'off') or (color == 'Off') or (color == 'OFF'):
            GPIO.output(bootGreenPin,0)
            GPIO.output(bootBluePin,0)
        else:
            print "Incorrect second argument in raptorStatusLights.status_lights. Enter only 'blue' or 'green' or 'off'."        
    else:
        print "Incorrect first argument in raptorStatusLights.status_lights. Enter only 'controller' or 'boot'."
