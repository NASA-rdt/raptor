#!/usr/bin/python
from driveRobotWill2 import RobotArm,Joint
import signal,sys
from InverseKinematics import goTo
import math
import os.input

robot = RobotArm();#this is the robot
	
#CREATE THE JOINTS HERE

	#Joint ( channel , name, min, max, default,min angle, max angle) 
gripper = Joint(8, 'gripper',120,680,400);  
wrist = Joint(6, 'wrist',120,680,400,-90,90);  
wrist_rotate2 = Joint(7, 'wrist_rotate2',130,680,400,-90,90);  
wrist_rotate = Joint(5, 'wrist_rotate',120,680,400,-90,90); 
elbow2 = Joint(4, 'elbow2',120,680,400,0,180);  
elbow = Joint(3, 'elbow',120,680,400,-90,90); 
shoulder = Joint(2, 'shoulder',120,680,400,-180,0); 
base = Joint(0, 'base',120,680,400,-90,90);  
	
	
#ADD THE JOINTS BELOW:  ORDER IS IMPORTANT!!
robot.addJoint(base);
robot.addJoint(shoulder);
robot.addJoint(elbow);
robot.addJoint(elbow2);
robot.addJoint(wrist_rotate);  
robot.addJoint(wrist);
robot.addJoint(wrist_rotate2);
robot.addJoint(gripper);

#speed =0.01
print 'Robot Arm Ready..'


while (True):
        ch = int(input("What channel?"))
        angle = int(input("What angle?"))
        if (angle < 130):
            angle = 120
        if (angle > 600):
            angle = 500
        if ch !=1:
                pwm.setPWM(ch, 0 ,angle)
            