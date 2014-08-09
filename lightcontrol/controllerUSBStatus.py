 #!/usr/bin/python

#Created by Aaron Neely for NASA GSFC SSCO internship summer 2014

# This script checks whether a supported controller is connected to the RAPTOR Edge arm kit
# and if any of the motors are currently being moved. It controls the controller status light accordingly

#Import libraries
import sys
import usb.core
import time
import threading
import Queue
import signal

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
vendor = [0x46d, 0x45e]
product = [0xc626, 0x28e]


z = True

length = len(vendor)
statusQueue = Queue.Queue()

class ControllerThread(threading.Thread):

        def __init__(self,q):
                self.q = q
                threading.Thread.__init__(self)
        def run(self):
                self.old_x = None
                while True:
                        self.x = False
                        for y in range(0, length):
                                dev = usb.core.find(idVendor = vendor[y], idProduct = product[y])
                                if dev is not None:
                                        self.x = True
                        if self.x != self.old_x:
                                self.q.put(self.x)
                                self.old_x = self.x


Thread = ControllerThread(statusQueue)
Thread.start()



def isConnected():
        if z:
                for y in range(0, length):
                        dev = usb.core.find(idVendor = vendor[y], idProduct = product[y])
                        if dev is not None:
                                x =  False
                z = False
        x = False
        if not statusQueue.empty():
                x = statusQueue.get()
        return x
                       
