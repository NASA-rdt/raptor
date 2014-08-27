#!/usr/bin/python
from driveRobotWill2 import RobotArm,Joint
from spnav import *
import signal,sys
from InverseKinematics import goTo
import math
import time



DEADZONE=220 #Deadzone for SpaceNav Controller


robot = RobotArm();#this is the robot
	
#CREATE THE JOINTS HERE

	#Joint ( channel , name, min, max, default) 
gripper = Joint(8, 'gripper',120,680,400);  
wrist = Joint(6, 'wrist',150,620,496,-math.pi/2,math.pi/2);  
wrist_rotate2 = Joint(7, 'wrist_rotate2',120,620,370,-math.pi/2,math.pi/2);  
wrist_rotate = Joint(5, 'wrist_rotate',145,600,288,-math.pi/2,math.pi/2); 
elbow2 = Joint(4, 'elbow2',150,640,400,0,math.pi);  
elbow = Joint(3, 'elbow',120,680,525,-math.pi/2,math.pi/2); 
shoulder = Joint(2, 'shoulder',120,590,450,-math.pi,0); 
base = Joint(0, 'base',200,660,400,-math.pi/2,math.pi/2);  
	
	
#ADD THE JOINTS BELOW:  ORDER IS IMPORTANT!!
robot.addJoint(base);
robot.addJoint(shoulder);
robot.addJoint(elbow);
robot.addJoint(elbow2);
robot.addJoint(wrist_rotate);  
robot.addJoint(wrist);
robot.addJoint(wrist_rotate2);
robot.addJoint(gripper);

spnav_open() # open spnav controller input
speed =0.05
print 'Robot Arm Ready..'
'''
currentPose = []#(0 , 0 , 0, 0 , 0 , 0, 0)
testPos = [math.pi/4,-math.pi/3,math.pi/3,math.pi/2,-math.pi/5,math.pi/6,math.pi/6]
for i in range(0,len(robot.joints)):
	if robot.joints[i].name is not 'gripper':
		currentPose.append(robot.joints[i].getMotorVals(testPos[i]))
print currentPose
'''
try:
	while True:
		event = spnav_poll_event()
		if event is not None:
			if event.ev_type == 1: #SPNAV Motion Events
				curDeltas = [0,0,0,0,0,0]
				#X Direction
				if event.translation[2] >= DEADZONE:
					curDeltas[0] = speed
				elif event.translation[2] <= -DEADZONE:
					curDeltas[0] = -speed
				elif event.translation[2] > -DEADZONE and event.translation[2] < DEADZONE:
					curDeltas[0] = 0

				#Y Direction
				if event.translation[0] >= DEADZONE:
					curDeltas[1] = speed
				elif event.translation[0] <= -DEADZONE:
					curDeltas[1] = -speed
				elif event.translation[0] > -DEADZONE and event.translation[1] < DEADZONE:
					curDeltas[1] = 0
				
				#Z Direction
				if event.translation[1] >= DEADZONE:
					curDeltas[2] = speed
				elif event.translation[1] <= -DEADZONE:
					curDeltas[2] = -speed
				elif event.translation[1] > -DEADZONE and event.translation[1] < DEADZONE:
					curDeltas[2] = 0
				
				#Move elbow joint via X-rotation  
				if event.rotation[0] >= DEADZONE:
					curDeltas[3] = speed
				elif event.rotation[0] <= -DEADZONE:
					curDeltas[3] = -speed
				elif event.rotation[0] > -DEADZONE and event.rotation[0] < DEADZONE:
					curDeltas[3] = 0

				#Move grip joint via Y-rotation
				if event.rotation[2] >= DEADZONE:
					curDeltas[4] = speed
				elif event.rotation[2] <= -DEADZONE:
					curDeltas[4] = -speed
				elif event.rotation[2] > -DEADZONE and event.rotation[2] < DEADZONE:
					curDeltas[4] = 0
				
				#Move base joint via Z-rotation
				if event.rotation[1] >= DEADZONE:
					curDeltas[5] = speed
				elif event.rotation[1] <= -DEADZONE:
					curDeltas[5] = -speed
				elif event.rotation[1] > -DEADZONE and event.rotation[1] < DEADZONE:
					curDeltas[5] = 0
				
				#Run Inverse Kinematics and change the motor values
				if curDeltas != [0,0,0,0,0,0]:
					#print curDeltas
					newPos = goTo(robot.getCurrentPose(),curDeltas,0)	
					#print 'robot current position'
					#print robot.getCurrentPose()
					zing = robot.goToXYZ(newPos)
					#print 'New Position'
					#print zing
					#print robot.getCurrentPose()
					#time.sleep(0.2)
					curDeltas = [0,0,0,0,0,0]

				spnav_remove_events(SPNAV_EVENT_MOTION)
				#print robot.getCurrentPose()
			

				
			elif event.ev_type == 2: #SPNAV Button Events
				if event.bnum == 0 and event.press:
					robot.getJoint('gripper').setSpeed(-9)
				elif event.bnum == 1 and event.press:
					robot.getJoint('gripper').setSpeed(9)
				else:
					robot.getJoint('gripper').setSpeed(0)

		spnav_remove_events(SPNAV_EVENT_ANY)
		


except KeyboardInterrupt:
	print '\nQuitting...'
finally:
	spnav_close()


