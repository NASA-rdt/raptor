#Created by Aaron Neely for NASA GSFC SSCO internship summer 2014

#!/usr/bin/python
import sys
import usb.core
import usb.util

#Create arrays to hold codes
vendor = []
product = []

print 'Script to find product and vendor IDs for input device. \n\n'

#Wait until device is disconnected to continue
x = raw_input('Disconnect input device. Hit Enter to continue.\n')

#Find all connected devices and add them to our arrays
dev = usb.core.find(find_all=True)
for cfg in dev:
    vendor.append(cfg.idVendor)
    product.append(cfg.idProduct)

#Wait until device is connected to continue
x = raw_input('Connect input device. Hit Enter to continue.')

#Find all connected devices again
dev = usb.core.find(find_all=True)
for cfg in dev:
    #Search through new list of devices and print any that weren't there the first time 
    if cfg.idVendor not in vendor:
        sys.stdout.write('\nYour Device:  VendorID = ' + hex(cfg.idVendor) + '  &  ProductID = ' + hex(cfg.idProduct))

print "\n\nAdd these codes to the 'vendor' and 'product' arrays in lightcontrol/controllerUSBStatus.py"
