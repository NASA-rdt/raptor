 #!/usr/bin/python

#Created by Aaron Neely for NASA GSFC SSCO internship summer 2014

# This script checks whether a supported controller is connected to the RAPTOR Edge arm kit
# and if any of the motors are currently being moved. It controls the controller status light accordingly

#Import libraries
import usb.core
import time
import raptorStatusLights as lights
import ConfigParser

config = ConfigParser.RawConfigParser()

#ADD DEVICE CODES HERE

vendor = [0x46d, 0x45e]
product = [0xc626, 0x28e]

length = len(vendor)



while True:

    time.sleep(.1)
    
    connected = False
    for y in range(0, length):
        dev = usb.core.find(idVendor = vendor[y], idProduct = product[y])
        if dev is not None:
            connected =  True

    config.read("/home/pi/RobotArmGit/armcontrol/ArmStatus.cfg")
    moving = config.getboolean('RobotArm','moving')

    if not connected:
        #print ("off")
        lights.status_lights('controller','off')
    elif connected and not moving:
        #print ("green")
        lights.status_lights('controller', 'green')
    elif connected and moving:
        #print ("blue")
        lights.status_lights('controller', 'blue')
