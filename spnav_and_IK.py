from spnav import *
import signal,sys
import InverseKinematics as InKin
import ForwardKinematics as ForKin
import math
import numpy as np
import time


DEADZONE = 220
damp = .003
transspeed = 1.0
rotspeed =   0.3


spnav_open()

theta = [np.pi/4,-np.pi/3,np.pi/3,np.pi/2,-np.pi/5,np.pi/6,np.pi/6]
EndPos = ForKin.FK(theta,1)
 


try:
	while True:
		event = spnav_poll_event()
		if event is not None:
			if event.ev_type == 1: #SPNAV Motion Events
				curDeltas = [0,0,0,0,0,0]
				#X Direction
				if event.translation[2] >= DEADZONE:
					curDeltas[0] = transspeed
				elif event.translation[2] <= -DEADZONE:
					curDeltas[0] = -transspeed
				elif event.translation[2] > -DEADZONE and event.translation[2] < DEADZONE:
					curDeltas[0] = 0

				#Y Direction
				if event.translation[0] >= DEADZONE:
					curDeltas[1] = -transspeed
				elif event.translation[0] <= -DEADZONE:
					curDeltas[1] = transspeed
				elif event.translation[0] > -DEADZONE and event.translation[1] < DEADZONE:
					curDeltas[1] = 0
				
				#Z Direction
				if event.translation[1] >= DEADZONE:
					curDeltas[2] = transspeed
				elif event.translation[1] <= -DEADZONE:
					curDeltas[2] = -transspeed
				elif event.translation[1] > -DEADZONE and event.translation[1] < DEADZONE:
					curDeltas[2] = 0
				
				#Move elbow joint via X-rotation  
				if event.rotation[0] >= DEADZONE:
					curDeltas[3] = rotspeed
				elif event.rotation[0] <= -DEADZONE:
					curDeltas[3] = -rotspeed
				elif event.rotation[0] > -DEADZONE and event.rotation[0] < DEADZONE:
					curDeltas[3] = 0

				#Move grip joint via Y-rotation
				if event.rotation[2] >= DEADZONE:
					curDeltas[4] = rotspeed
				elif event.rotation[2] <= -DEADZONE:
					curDeltas[4] = -rotspeed
				elif event.rotation[2] > -DEADZONE and event.rotation[2] < DEADZONE:
					curDeltas[4] = 0
				
				#Move base joint via Z-rotation
				if event.rotation[1] >= DEADZONE:
					curDeltas[5] = rotspeed
				elif event.rotation[1] <= -DEADZONE:
					curDeltas[5] = -rotspeed
				elif event.rotation[1] > -DEADZONE and event.rotation[1] < DEADZONE:
					curDeltas[5] = 0
				
				#Run Inverse Kinematics and change the motor values
				if curDeltas != [0,0,0,0,0,0]:
					print curDeltas
					newtheta = InKin.goTo(theta,curDeltas,1,damp)
					if math.isnan(newtheta[2]) is False:
						theta = newtheta
					else:
						print 'returned NAN, setting old theta'
					EndPos = ForKin.FK(theta,1)
					print EndPos




				spnav_remove_events(SPNAV_EVENT_MOTION)
				#print robot.getCurrentPose()
				time.sleep(0.2)


			'''	
			elif event.ev_type == 2: #SPNAV Button Events
				if event.bnum == 0 and event.press:
					
					#robot.getJoint('gripper').setSpeed(-9)
				elif event.bnum == 1 and event.press:
					#robot.getJoint('gripper').setSpeed(9)
				else:
					#robot.getJoint('gripper').setSpeed(0)
			'''
		spnav_remove_events(SPNAV_EVENT_ANY)




except KeyboardInterrupt:
	print '\nQuitting...'
finally:
	
	spnav_close()
