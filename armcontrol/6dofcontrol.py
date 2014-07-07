#!/usr/bin/python

# Python script for controlling the OWI Robotic Arm using a Xbox 360 controller
#
# Version 1.0 - 05/01/2013
# Created by Matt Dyson: http://mattdyson.org

# We require the lego-pi xbox_read class - https://github.com/zephod/lego-pi
from legopi.lib import xbox_read
# We also require the RobotArm class - http://mattdyson.org/projects/robotarm
from armcontrol import RobotArm

# So we can catch Ctrl+C
import signal
import sys


# The deadzone within which we ignore inputs, approximately 1/3 of total possible input
DEADZONE = 12000

"Fetch the name of the motor mapped to the 'key' axis"
def getMotor(key):
	return {ller"
	sys.exit(0)

# Capture Ctrl+C so we can shut down nicely
signal.signal(signal.SIGINT, signal_handler)

print "Starting RobotArm Controller"
print "Press Ctrl+C at any time to quit"

		'X1':'base',
		'Y1':'shoulder',
		'X2':'wristrotate',
		'Y2':'elbow',
		'RB':'grip', #RB is close
		'LB':'grip', #LB is open
		'RT':'wrist', #RT is up
		'LT':'wrist' #LT is down
	}.get(key,None)

def signal_handler(signal, frame):
	print "Stopping RobotArm Controller"
# Create our RobotArm
arm = RobotArm.RobotArm()

# Our main event loop
for event in xbox_read.event_stream(deadzone=DEADZONE):
	#print "Xbox event: %s" % (event)
	
	#Special case directions for RB and LB, as we want the grip to move depending on which is used
	if(event.key=='RB'):
		if(event.value>0)
			direction=1
		else:
			direction=0
	elif(event.key=='LB'):
		if (event.value>0)
			direction=-1
		else:
			direction=0

	# Special case directions for RT and LT, as we want the wrist to move depending on which is used
	if(event.key=='RT'):
		direction=1
	elif(event.key=='LT'):
		direction=2
	else:
		# For all other cases, base direction on the value (negative = up, positive = down)
		if(event.value<0):
			direction = -1
		elif(event.value>0):
			direction = 1
	
	# If our axis has returned to zero, then stop moving
	if(event.value==0):
		direction = 0

	# Fetch the motor to act on
	motor = getMotor(event.key)

	if(motor is not None):
		try:
			# Pass on the instruction to the RobotArm
			arm.moveMotor(motor,direction)
		except:
			print "Could not issue command to RobotArm"
			raise
	else:
		print "I don't know how to move motor '%s'" % (motor) 
