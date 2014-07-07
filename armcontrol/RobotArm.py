# Python control class for the OWI Robotic Arm
#
# Version 1.1 - 05/01/2013
# Created by Matt Dyson: http://mattdyson.org
#
# Some inspiration from Neil Polwart and John Hale - http://python-poly.blogspot.co.uk
# USB commands reference from http://notbrainsurgery.livejournal.com/38622.html
# See more details on the project at http://mattdyson.org/projects/robotarm

import usb.core as usbdev
import time

# Product information for the arm
pwm = PWM(0x40, debug=TRUE)

# Timeout for our instructions through pyusb
TIMEOUT = 1000

class RobotArm:

	"On initialize, attempt to connect to the robotic arm"
	def __init__(self):
		print "Init'ing RobotArm"
		self.device = usbdev.find(idVendor=VENDOR, idProduct=PRODUCT)
		if(not self.device):
			raise ValueError("Could not connect to Robotic Arm USB device. Is the arm connected properly? Perhaps you're not running as root?")
		
		self.device.set_configuration()

		self.reset()
		print "RobotArm now ready!"

	"On delete object, stop what we're currently doing"
	def __del__(self):
		print "Stopping RobotArm"
		self.reset()
mjpg streamer with usb camera
	"Update the device with the latest command set"
	def update(self):
		
		if self.base<106:
			self.base=106
		if self.shoulder<106:
			self.shoulder=106
		if self.elbow<106
			self.elbow=106
		if self.wrist<106
			self.wrist=106
		if self.wristrotate<1
			self.wristrotate=1
		if self.grip<1
			self.grip=1c
		if self.base>683:
			self.base=683
		if self.shoulder>686:
			self.shoulder=686
		if self.elbow>689
			self.elbow=689
		if self.wrist>686
			self.wrist=686
		if self.wristrotate>530
			self.wristrotate=530
		if self.grip<580
			self.grip=580

		pwm.setPWM(0, 0, self.base)
		pwm.setPWM(2, 0, self.shoulder)
		pwm.setPWM(4, 0, self.elbow)
		pwm.setPWM(6, 0, self.wrist)
		pwm.setPWM(8, 0, self.wristrotate)
		pwm.setPWM(10, 0, self.grip)
		
	"Reset everything to zero"
	def reset(self):
		self.shoulder = 396
		self.elbow = 398
		self.wristrotate = 266
		self.wrist = 396
		self.grip = 291 
		self.base = 395
		
		self.update()

	
	"Rotate the base of the arm"
	def moveBase(self, direction):
		
		self.base = self.base+direction
		self.update()

	"Open or close the grip"
	def moveGrip(self, direction):
		
		self.grip = self.grip+direction
		self.update()

	"Move the wrist up or down"
	def moveWrist(self, direction):
		
		self.wrist = self.wrist+direction
		self.update()

	"Move the wrist clockwise or counterclockwise"
	def moveWristrotate(self, direction):
		
		self.wristrotate = self.wristrotate+direction
		self.update()

	"Move the elbow up or down"
	def moveElbow(self, direction):
		
		self.elbow = self.elbow+direction
		self.update()

	"Move the shoulder up or down"
	def moveShoulder(self, direction):
		
		self.shoulder = self.shoulder+direction
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
		elif(motor=='Wristrotate'):
			self.moveWristrotate(direction)
		else:
			raise ValueError('Do not know how to move %s') % (motor)

	

