#!/usr/bin/python

#Created by Aaron Neely for NASA GSFC SSCO internship summer 2014

# This script checks whether a supported controller is connected to the RAPTOR Edge arm kit
# It controls the controller status light accordingly

#Import libraries
import time
import ConfigParser
import subprocess
import raptorStatusLights as lights

controllers = ['Xbox', 'Space']
length = len(controllers)

while True:
    status = 0
    devices = subprocess.check_output("lsusb", shell=True)
    for y in range(0, length):
        if controllers[y] in devices:
            status = 1

    lights.status_lights('controller','green',status)

