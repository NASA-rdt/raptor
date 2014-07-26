# Python control class for the OWI Robotic Arm
#
# Version 1.1 - 05/01/2013
# Created by Matt Dyson: http://mattdyson.org
#
# Some inspiration from Neil Polwart and John Hale - http://python-poly.blogspot.co.uk
# USB commands reference from http://notbrainsurgery.livejournal.com/38622.html
# See more details on the project at http://mattdyson.org/projects/robotarm

# Modified for NASA GSFC Summer internship 2014 by Aaron Neely

import usb.core as usbdev
import time
import RPi.GPIO as GPIO

#  Controller status green and blue pins
greenLightPin=23
blueLightPin=24

#  GPIO Setup for lights
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(greenLightPin,GPIO.OUT)
GPIO.setup(blueLightPin,GPIO.OUT)

# Product information for the arm
VENDOR = 0x1267
PRODUCT = 0x0000

# Timeout for our instructions through pyusb
TIMEOUT = 1000

class RobotArm:

	"On initialize, attempt to connect to the robotic arm"
	def __init__(self):
		#print "Init'ing RobotArm"
		self.first = 1
		#print self.first
		self.device = usbdev.find(idVendor=VENDOR, idProduct=PRODUCT)
		if(not self.device):
			raise ValueError("Could not connect to Robotic Arm USB device. Is the arm connected properly? Perhaps you're not running as root?")
		
		self.device.set_configuration()

		self.reset()
		#print "RobotArm now ready!"

	"On delete object, stop what we're currently doing"
	def __del__(self):
		#print "Stopping RobotArm"
		self.reset()

	"Update the device with the latest command set"
	def update(self):
		cmd = self.buildCommand()
		#print "Sending command %r to RobotArm" % (cmd)
		self.device.ctrl_transfer(0x40, 6, 0x100, 0, cmd, TIMEOUT)

	"Build a command set from our current values"
	def buildCommand(self):
		bytes = [0] * 3
		bytes[0] = (self.shoulder<<6) + (self.elbow<<4) + (self.wrist<<2) + self.grip
		bytes[1] = self.rotate
		bytes[2] = self.light

		# If no motors are moving, turn the controller status light green
		if bytes == [0,0,0] or bytes == [0,0,1]:
		    	GPIO.output(greenLightPin,1)
		    	GPIO.output(blueLightPin,0)
                # If motors are moving, turn the controller status light blue
		else:
		    	GPIO.output(greenLightPin,0)
		   	GPIO.output(blueLightPin,1)
		# Prevent the controller status light from turning on before
		# anything is sent
		if self.first == 1:
			GPIO.output(greenLightPin,0)
			self.first = 0
		#print self.first
		#print bytes
		return bytes
	
	"Reset everything to zero"
	def reset(self):
		self.shoulder = 0
		self.elbow = 0
		self.wrist = 0
		self.grip = 0
		self.rotate = 0
		self.light = 0

		self.update()

	"Set the light to the opposite of whatever it's on currently"
	def toggleLight(self):
		self.light = (1,0)[self.light==1]
		self.update()

	"Turn the light on or off"
	def setLight(self,lightVal):
		if(lightVal not in range(0,2)):
			raise ValueError('Light can only be set to off (0) or on (1)')

		self.light = lightVal
		self.update()

	"Rotate the base of the arm"
	def moveBase(self, direction):
		if(direction not in range(0,3)):
			raise ValueError('Base can only be set to stop (0), clockwise (1) or counter-clockwise (2)')

		self.rotate = direction
		self.update()

	"Open or close the grip"
	def moveGrip(self, direction):
		if(direction not in range(0,3)):
			raise ValueError('Grip can only be set to stop (0), close (1) or open (2)')

		self.grip = direction
		self.update()

	"Move the wrist up or down"
	def moveWrist(self, direction):
		if(direction not in range(0,3)):
			raise ValueError('Wrist can only be set to stop (0), up (1) or down (2)')

		self.wrist = direction
		self.update()

	"Move the elbow up or down"
	def moveElbow(self, direction):
		if(direction not in range(0,3)):
			raise ValueError('Elbow can only be set to stop (0), up (1) or down (2)')

		self.elbow = direction
		self.update()

	"Move the shoulder up or down"
	def moveShoulder(self, direction):
		if(direction not in range(0,3)):
			raise ValueError('Shoulder can only be set to stop (0), up (1) or down (2)')

		self.shoulder = direction
		self.update()

	"Convenience method for moving motors by name"
	def moveMotor(self, motor, direction):
		if(motor=='base'):
			self.moveBase(direction)
		elif(motor=='shoulder'):
			self.moveShoulder(direction)
		elif(motor=='elbow'):
			self.moveElbow(direction)
		elif(motor=='wrist'):
			self.moveWrist(direction)
		elif(motor=='grip'):
			self.moveGrip(direction)
		else:
			raise ValueError('Do not know how to move %s') % (motor)

	
	"Flash the light 'iterations' times, with a gap of 'interval' between each"
	def flashLight(self, iterations, interval):
		for i in range(iterations):
			self.setLight(1)
			time.sleep(interval)
			self.setLight(0)
			time.sleep(interval)
