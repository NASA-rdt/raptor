#!/usr/bin/python

#Created by Aaron Neely for NASA GSFC SSCO internship summer 2014

# This script creates a function to check whether a supported controller is connected to the RAPTOR Edge arm kit

#Import libraries
import sys
import usb.core
import time
from array import array

#IDs for SpaceNav
#  SN_Vendor = 0x46d
#  SN_Product = 0xc626

#IDs for XboxController
#  XC_Vendor = 0x45e
#  XC_Product = 0x28e






#ADD DEVICE CODES HERE

#To add new supported device, add its vendorID to the end of the
#vendor array and its productID to the end of the product array
# - THEY MUST BE IN THE SAME POSITIONS IN THEIR RESPECTIVE ARRAYS
vendor = array('l',[0x46d, 0x45e])
product = array('l',[0xc626, 0x28e])







# Function to detect if a supported controller is connected
def connected():
    #find all USB devices
    dev = usb.core.find(find_all=True)

    x=False
    #loop through devices
    for cfg in dev:
        #detect if any of the devices match the vendor and product ID sets in our array
        for y in range(0, len(vendor)):
            if (cfg.idVendor == vendor[y]) and (cfg.idProduct == product[y]): 
                x = True
                return x
            else:
                x = False
    return x

#if __name__ == '__main__':
#    x = connected()
#    print x
