# Modified for NASA GSFC Summer internship 2014 by Aaron Neely

# Pull libraries
import time
import os
from sys import stdin
import re
import RPi.GPIO as GPIO
from evdev import InputDevice, categorize, ecodes

#  Controller status green and blue pins
greenLightPin=23
blueLightPin=24

#  GPIO setup for lights
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(greenLightPin,GPIO.OUT)
GPIO.setup(blueLightPin,GPIO.OUT)

#Start up xboxdrv driver
#os.system('(sudo xboxdrv -d -D -s --dbus disabled)&')
#time.sleep(2)

#Setup for evdev
#dev = InputDevice('/dev/input/event2')
#print(dev)

#s = re.compile('[ :]')

class Event:
    def __init__(self,key,value,old_value):
        self.key = key
        self.value = value
        self.old_value = old_value
    def is_press(self):
       return self.value==1 and self.old_value==0
    def __str__(self):
        return 'Event(%s,%d,%d)' % (self.key,self.value,self.old_value)

#Map evdev button codes to button keys
def code2key(code):
    return {
            0:'X1',
            1:'Y1',
            3:'X2',
            4:'Y2',
            9:'RT',
            10:'LT',
            310:'LB',
            311:'RB',
            304:'A',
            305:'B',
            307:'X',
            308:'Y',
            314:'select',
            315:'start',
            316:'xbox',
            317:'LS',
            318:'RS'
            }.get(code,None)
def apply_deadzone(x, deadzone, scale):
    if x < 0:
        return (scale * min(0,x+deadzone)) / (32768-deadzone)
    return (scale * max(0,x-deadzone)) / (32768-deadzone)

def event_stream(deadzone=0,scale=32768):
    #_data = None
    old_value=None
    x=0
    
    #Start up xboxdrv driver
    subprocess = os.popen('sudo xboxdrv -d -D -v --dbus disabled','r',65536)
    time.sleep(1)
    #Setup for evdev
    dev = InputDevice('/dev/input/event2')
    print(dev)

    while True:
        line = subprocess.readline()
        # Turn off controller status light if controller is disconnected
        if 'failed' in line:
	    GPIO.output(greenLightPin,GPIO.LOW)
	    print (line)
            #raise ValueError(line)
        #Turn on controller status light if controller is reconnected
	if 'controller connected' in line:
	    GPIO.output(greenLightPin,GPIO.HIGH)
	    print(line)

        #Run loop for each new evdev event
        for evdev_event in dev.read_loop():
            value = None
            #Convert evdev event code into xbox key
            key=code2key(evdev_event.code)

            #Special condition for X1 because it sends every other value as 0
            if evdev_event.code == 0:
	        if evdev_event.value != 0:
	        	value = apply_deadzone(evdev_event.value,deadzone,scale)
            #Special conditions for joysticks
            elif evdev_event.code == 1 or evdev_event.code == 3 or evdev_event.code == 4:
            	value = apply_deadzone(evdev_event.value,deadzone,scale)
            #Special conditions for RT and LT
            elif evdev_event.code == 9 or evdev_event.code == 10:
                #Adds trigger deadzone of 125 (out of 255)
                if evdev_event.value >= 125:
                    value=1
                else:
                    value=0
            else:
                value=evdev_event.value

            #Returns event data if different
            if value != None:
                event = Event(key,value,old_value) 
                #print(value)
                yield event
                old_value = value








#        data = filter(bool,s.split(line[:-1]))
#
#	if len(data)==42:
#           # Break input string into a data dict
#            data = { data[x]:int(data[x+1]) for x in range(0,len(data),2) }
#	    if not _data:
#                _data = data
#                continue
#            for key in data:
#                if key=='X1' or key=='X2' or key=='Y1' or key=='Y2':
#                    data[key] = apply_deadzone(data[key],deadzone,scale)
#                if data[key]==_data[key]: continue
#                event = Event(key,data[key],_data[key])
#                yield event
#            _data = data

# Appendix: Keys
# --------------
# X1
# Y1
# X2
# Y2
# du
# dd
# dl
# dr
# back
# guide
# start
# TL
# TR
# A
# B
# X
# Y
# LB
# RB
# LT
# RT
