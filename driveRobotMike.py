#! /usr/bin/python
import usb.core as usbdev
#from legopi.lib.Adafruit_PWM_Servo_Driver import PWM
#from legopi.lib import xbox_read
import time, thread
#from InverseKinematics import goTo
import numpy as np
import math

# Product information for the arm
#pwm = PWM(0x40, debug=True)



#ALL OF THIS IS IN RADIANS. DO NOT USE DEGREES FOR ANYTHING. EVER. AT ALL. 



class Joint:
	def __init__(self,channel,name,minVal,maxVal,defVal = 0, minAng = 0, maxAng = 0,angleOff = 0):
		self.channel = channel;
		self.name = name;
		self.minVal = minVal;
		delf.maxVal = maxVal;
		self.defVal = defVal;
		self.currentVal = defVal;
		self.minAng = minAng;
		self.maxAng = maxAng;
		self.angleOff = angleOff;
		self.speed = 0;
		self.changed = True;
	def setSpeed(self,speed):
		self.speed = speed;
	def toString(self):
		return "Joint('%s')=%d @ %d" % (self.name, self.currentVal,self.speed);
	def set(self,value):
		if value > self.maxVal:
			value = self.maxVal;
		if value < self.minVal:
			value = self.minVal;
		self.currentVal = value;
		self.changed = True;
	def reset(self):
		self.set(defVal);
	def delta(self,inc):
		if inc != 0:
			self.set(self.currentVal + inc);
	def write(self,val):
		if self.changed:
			#print 'Writing',val,'to',self.name
#			pwm.setPWM(self.channel,0,self.currentVal);
			self.changed=False
	def update(self):
		#print 'updating',self.name;
		self.delta(self.speed);
		self.write(self.currentVal);
	def getRadians(self):
		rads = self.minAng + (self.maxAng - self.minAng) * ((self.currentVal - self.minVal) / (self.maxVal - self.minVal))
		return rads
	def getMotorVals(self,radVal):
		newVal = self.minVal + (self.maxVal - self.minVal) * ((radVal - self.minAng) / (self.maxAng - self.minAng))
		return int(newVal)

class RobotArm:
	def __init__