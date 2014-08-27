# Python control class for the OWI Robotic Arm
#
# Version 1.1 - 05/01/2013
# Created by Matt Dyson: http://mattdyson.org
#
# Some inspiration from Neil Polwart and John Hale - http://python-poly.blogspot.co.uk
# USB commands reference from http://notbrainsurgery.livejournal.com/38622.html
# See more details on the project at http://mattdyson.org/projects/robotarm

import usb.core as usbdev
from Adafruit_PWM_Servo_Driver import PWM
import time

# Product information for the arm
pwm = PWM(0x40, debug=True)

# Timeout for our instructions through pyusb
TIMEOUT = 1000

class RobotArm:

	"On initialize, attempt to connect to the robotic arm"
	def __init__(self):

		self.reset()
		print "RobotArm now ready!"

	"On delete object, stop what we're currently doing"
	def __del__(self):
		print "Stopping RobotArm"
		self.reset()
	"Update the device with the latest command set"
	def update(self):
		
		"""if self.base<106:
			self.base=106
		if self.shoulder<106:
			self.shoulder=106
		if self.elbow<106:
			self.elbow=106
		if self.wrist<106:
			self.wrist=106
		if self.wristrotate<1:
			self.wristrotate=1
		if self.grip<1:
			self.grip=1
		if self.base>683:
			self.base=683
		if self.shoulder>686:
			self.shoulder=686
		if self.elbow>689:
			self.elbow=689
		if self.wrist>686:
			self.wrist=686
		if self.wristrotate>530:
			self.wristrotate=530
		if self.grip>580:
			self.grip=580"""

		pwm.setPWM(0, 0, self.basePos)
		pwm.setPWM(1, 0, self.shoulderPos)
		pwm.setPWM(2, 0, self.elbowPos)
		pwm.setPWM(3, 0, self.wristPos)
		pwm.setPWM(4, 0, self.wristrotatePos)
		pwm.setPWM(5, 0, self.gripPos)
		
	"Reset everything to zero"
	def reset(self):
		self.shoulderPos = 396
		self.elbowPos = 398
		self.wristrotatePos = 266
		self.wristPos = 396
		self.gripPos = 291 
		self.basePos = 395
		
		self.update()

	
	"Rotate the base of the arm"
	def setBase(self, position):
		
		self.basePos = position
		self.update()

	"Open or close the grip"
	def setGrip(self, position):
		
		self.gripPos = position
		self.update()

	"Move the wrist up or down"
	def setWrist(self, position):
		
		self.wrist = position
		self.update()

	"Move the wrist clockwise or counterclockwise"
	def setWristrotate(self, position):
		
		self.wristrotate = position
		self.update()

	"Move the elbow up or down"
	def setElbow(self, position):
		
		self.elbow = position
		self.update()

	"Move the shoulder up or down"
	def setShoulder(self, position):
		
		self.shoulder = position
		self.update()

	