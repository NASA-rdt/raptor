#!/usr/bin/python
import usb.core as usbdev
from legopi.lib.Adafruit_PWM_Servo_Driver import PWM
from legopi.lib import xbox_read
import time, thread
from InverseKinematics import goTo
import numpy as np

# Product information for the arm
pwm = PWM(0x40, debug=True)


class Joint:
	def __init__(self, channel, name, minVal, maxVal, defVal = 0, angleOff = 0):
                self.channel = channel;
		self.name = name;
		self.minVal = minVal;
		self.maxVal = maxVal;
		self.defVal = defVal;
		self.currentVal = defVal;
		self.angelOff = angleOff
		self.speed = 0;
		self.changed=True;
	def setSpeed(self, speed):
		self.speed = speed;
	def toString(self):
		return "Joint('%s')=%d @ %d" % (self.name,self.currentVal,self.speed);
	def set(self, value):
		if value > self.maxVal:
			value = self.maxVal;
		if value < self.minVal:
			value = self.minVal;
		self.currentVal = value;
		self.changed=True;
	def reset(self):
		self.set(defVal);
	def delta(self, inc):
                if inc != 0:
                        self.set(self.currentVal+inc);
	def write(self,val): 
                if self.changed:
                        #print 'Writing',val,'to',self.name
                	pwm.setPWM(self.channel, 0, self.currentVal);
                        self.changed=False
                
	def update(self):
		#print 'Updating',self.name;
		self.delta(self.speed);
		self.write(self.currentVal);
	"""def getDegrees(self):
                value = self.currentVal - self.defVal
                map(self.currentVal, self.minVal, self.maxVal, 
                return self.currentVal #map this value into degrees somehow such as:(1024 = 2*np.pi ...."""
                
class RobotArm:

	def __init__(self, delay = 0.05):
		self.joints = [];
		thread.start_new_thread( self.run, (delay,));
		self.running = True;
	def addJoint( self, joint):
		self.joints.append(joint);
		return self.joints.index(joint);

	def setJoint( self, joint , value ):
		self.joints.get(joint).set(value);

	def getJoint(self, name ):
		try:
			index = int(name)
			if name < len(self.joints):
				return self.joints[index];
			return None
		except ValueError:
			for joint in self.joints:
				if joint.name == name:
					return joint;
			return None;#check for null
	def setChanged(self):
                self.changed=True;
	def update(self):
                for joint in self.joints:
                        joint.update();
			
	def run( self, delay):
	        self.running = True;
	        while self.running:
	                time.sleep(delay);
                	self.update();
        def getCurrentPose(self):
                currentPose = []#(0 , 0 , 0, 0 , 0 , 0, 0)
                index = 0;
                for joint in self.joints:
                        currentPose.append(joint.getDegrees())
                print 'current Pose:',currentPose
                #add some way to get the angles from the motors and return it in a vector using ()
                return currentPose
        def goToXYZ(self,desiredDeltaPose):
                currentPose = self.getCurrentPose()
                print 'desired change in pose:',desiredDeltaPose
                goTo(currentPose, desiredDeltaPose)
