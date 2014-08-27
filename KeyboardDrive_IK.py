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
wrist = Joint(6, 'wrist',120,680,496,-90,90);  
wrist_rotate2 = Joint(7, 'wrist_rotate2',130,680,493,-90,90);  
wrist_rotate = Joint(5, 'wrist_rotate',120,680,288,-90,90); 
elbow2 = Joint(4, 'elbow2',120,680,400,0,180,1);  
elbow = Joint(3, 'elbow',120,680,218,-90,90); 
shoulder = Joint(2, 'shoulder',120,680,493,-180,0); 
base = Joint(0, 'base',120,680,540,-90,90);  
	
	
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
speed =0.1
print 'Robot Arm Ready..'
#testor = 1
#crap = 0

currentPose = []#(0 , 0 , 0, 0 , 0 , 0, 0)
testPos = [math.pi/4,-math.pi/3,-math.pi/3,math.pi/2,-math.pi/5,math.pi/6,math.pi/6]
for i in range(0,len(robot.joints)):
	if robot.joints[i].name is not 'gripper':
		currentPose.append(robot.joints[i].getMotorVals(testPos[i]))
print currentPose



try:
	while True:



		curDeltas = input('delta vector  =  ')
				
		#Run Inverse Kinematics and change the motor values
		#if testor == 1 and crap == 1:
		if curDeltas is not [0,0,0,0,0,0]:
			newPos = goTo(robot.getCurrentPose(),curDeltas,1)
			zing = robot.goToXYZ(newPos)
			print zing
			print robot.getCurrentPose()
			#testor = 0
			#crap = 0
		
				






except KeyboardInterrupt:
	print '\nQuitting...'
