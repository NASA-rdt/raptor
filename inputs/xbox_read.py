# Modified for NASA GSFC Summer internship 2014 by Aaron Neely

# Pull libraries
import time
import glob
import os
from sys import stdin
import re
from evdev import InputDevice, categorize, ecodes

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
    old_value=None
    x=0
    
    
    #Setup for evdev
    devicesNow = glob.glob('/dev/input/event*')
    found = False
    device = None
    for dev in devicesNow:
        device = InputDevice(dev)
       # print device.name
        if 'Xbox' in device.name:
            #print 'Found:',device.name,'on',dev
            found = True;
            break
    if not found:
        #print 'Xbox controller not found'
        return
    
    while True:
        #Run loop for each new evdev event
        for evdev_event in device.read_loop():
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
