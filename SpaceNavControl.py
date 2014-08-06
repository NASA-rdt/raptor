#!/usr/bin/python

# Python script for controlling the OWI Robotic Arm using a Space Navigator
#
# Version 1.1 - 07/18/2014
# Created by NASA RDT INTERNS


# We also require the RobotArm class - http://mattdyson.org/projects/robotarm
from armcontrol import RobotArm
# Import spnav lib to read from Space Navigator
from spnav import *

# So we can catch Ctrl+C
import signal
import sys

# The deadzone within which we ignore inputs, approximately 1/3 of total possible input
DEADZONE = int(200)
direction = 0

# Create our RobotArm
arm = RobotArm.RobotArm()

#Open spnav for events and start main loop
spnav_open()


try:
	while True:
		event = spnav_poll_event()
		if event is not None:
			if event.ev_type == 1:
			
				#Move shoulder joint via Y-translation
				if event.translation[2] >= DEADZONE:
					arm.moveMotor('shoulder',2)
				elif event.translation[2] <= -DEADZONE:
					arm.moveMotor('shoulder',1)
				elif event.translation[2] > -DEADZONE and event.translation[2] < DEADZONE:
					arm.moveShoulder(0)

				#Move elbow joint via X-rotation
				if event.rotation[0] >= DEADZONE:
					arm.moveMotor('elbow',1)
				elif event.rotation[0] <= -DEADZONE:
					arm.moveMotor('elbow',2)
				elif event.rotation[0] > -DEADZONE and event.rotation[0] < DEADZONE:
					arm.moveElbow(0)

				#Move wrist joint via Z-translation
				if event.translation[1] >= DEADZONE:
					arm.moveMotor('wrist',1)
				elif event.translation[1] <= -DEADZONE:
					arm.moveMotor('wrist',2)
				elif event.translation[1] > -DEADZONE and event.translation[1] < DEADZONE:
					arm.moveWrist(0)

				#Move base joint via Z-rotation
				if event.rotation[1] >= DEADZONE:
					arm.moveMotor('base',1)
				elif event.rotation[1] <= -DEADZONE:
					arm.moveMotor('base',2)
				elif event.rotation[1] > -DEADZONE and event.rotation[1] < DEADZONE:
					arm.moveBase(0)

				#Move grip joint via Y-rotation
				if event.rotation[2] >= DEADZONE:
					arm.moveMotor('grip',1)
				elif event.rotation[2] <= -DEADZONE:
					arm.moveMotor('grip',2)	
				elif event.rotation[2] > -DEADZONE and event.rotation[2] < DEADZONE:
					arm.moveGrip(0)

				spnav_remove_events(SPNAV_EVENT_MOTION)

			elif event.ev_type == 2:
				#print event.ev_type
				#Toggle Light	
				if event.bnum == 0:
					arm.toggleLight()
				
				
				#Set Light on/off
				if event.bnum == 1 and event.press:
					if direction == 1:					
						direction=0
					else:
						direction=1
					arm.setLight(direction)
				
                
except KeyboardInterrupt:
	print '\nQuitting...'
finally:
	spnav_close()

