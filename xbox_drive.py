#!/usr/bin/python
import usb.core as usbdev
from driveRobotWill2 import RobotArm, Joint
from legopi.lib.Adafruit_PWM_Servo_Driver import PWM
from legopi.lib import xbox_read
import time, thread
DEADZONE=15000

def main():
	robot = RobotArm();#this is the robot
	print "Creating Joints now..."
	#CREATE THE JOINTS HERE
	        #Joint ( channel , name, min, max, default) 
	gripper = Joint(8, 'gripper',120,400,135);   #BLANK
	wrist = Joint(6, 'wrist',120,680,400);  #Y/P
	wrist_rotate2 = Joint(7, 'wrist_rotate2',130,680,400);  #B/P
	wrist_rotate = Joint(5, 'wrist_rotate',120,680,400);  #rubberband
	elbow2 = Joint(4, 'elbow2',120,680,400);   #B/Y
	elbow = Joint(3, 'elbow',125,680,400);  #P
	shoulder = Joint(2, 'shoulder',200,680,400);  #B
	base = Joint(0, 'base',150,680,400);  #Y
	
	print "Adding Joints"
	#ADD THE JOINTS BELOW:
	robot.addJoint(base);
	robot.addJoint(shoulder);
	robot.addJoint(elbow);
	robot.addJoint(elbow2);
	robot.addJoint(wrist);
	robot.addJoint(gripper);
	robot.addJoint(wrist_rotate);    
	
	robot.addJoint(wrist_rotate2);
	print "starting Loop"
	loop( robot )

def loop( robot ):	
	for event in xbox_read.event_stream(deadzone = DEADZONE):
		#print "Xbox event: %s" % (event);
		if event.key == 'X1':
			if event.value > DEADZONE:
				robot.getJoint('base').setSpeed(-8);
				
			elif event.value < -DEADZONE:
				robot.getJoint('base').setSpeed(8);
				
			else:
				joint = robot.getJoint('base').setSpeed(0); 

		if event.key == 'Y1':
			if event.value > DEADZONE:
				robot.getJoint('shoulder').setSpeed(6);
	
			elif event.value < -DEADZONE:
				robot.getJoint('shoulder').setSpeed(-6);
				#print "setting speed -3"
			else:
				robot.getJoint('shoulder').setSpeed(0);
		
		if event.key == 'X2':
			if event.value > DEADZONE:
				robot.getJoint('wrist_rotate2').setSpeed(-6);
	
			elif event.value < -DEADZONE:
				robot.getJoint('wrist_rotate2').setSpeed(6);
				#print "setting speed -3"
			else:
				robot.getJoint('wrist_rotate2').setSpeed(0);
	
		if event.key == 'Y2':
			if event.value > DEADZONE:
				robot.getJoint('elbow').setSpeed(-6);
	
			elif event.value < -DEADZONE:
				robot.getJoint('elbow').setSpeed(6);
				#print "setting speed -3"
			else:
				robot.getJoint('elbow').setSpeed(0);
	
		if event.key == 'LB':
			if event.value == 1:
				robot.getJoint('elbow2').setSpeed(-6);
	
			else:
				robot.getJoint('elbow2').setSpeed(0);
	
		if event.key == 'RB':
			if event.value == 1:
				robot.getJoint('elbow2').setSpeed(6);
	
			else:
				robot.getJoint('elbow2').setSpeed(0);
	
		if event.key == 'LT':
			if event.value > 150:
				robot.getJoint('gripper').setSpeed(9);
	
			else:
				robot.getJoint('gripper').setSpeed(0);
	
		if event.key == 'RT':
			if event.value > 150:
				robot.getJoint('gripper').setSpeed(-9);
	
			else:
				robot.getJoint('gripper').setSpeed(0);
	
		if event.key == 'du':
			if event.value == 1:
				robot.getJoint('wrist').setSpeed(6);
	
			else:
				robot.getJoint('wrist').setSpeed(0);
	
		if event.key == 'dd':
			if event.value == 1:
				robot.getJoint('wrist').setSpeed(-6);
	
			else:
				robot.getJoint('wrist').setSpeed(0);
	
		if event.key == 'dr':
			if event.value == 1:
				robot.getJoint('wrist_rotate').setSpeed(-6);
	
			else:
				robot.getJoint('wrist_rotate').setSpeed(0);
	
		if event.key == 'dl':
			if event.value == 1:
				robot.getJoint('wrist_rotate').setSpeed(6);
	
			else:
				robot.getJoint('wrist_rotate').setSpeed(0);
	
	
		
	        """if event.key == 'X':
	                if event.value == 1:
	                        robot.getJoint('shoulder').set(325);
	                        robot.getJoint('elbow').set(230);
	                        robot.getJoint('elbow2').set(325);
	                        robot.getJoint('wrist').set(420);
	                        robot.getJoint('wrist_rotate').set(200);
	                        robot.getJoint('wrist_rotate2').set(350);
	                        
	                else:
	                        robot.getJoint('wrist_rotate').setSpeed(0);
	
		if event.key == 'B':
	                if event.value == 1:
	                        robot.getJoint('shoulder').set(270);
	                        robot.getJoint('elbow').set(450);
	                        robot.getJoint('elbow2').set(400);
	                        robot.getJoint('wrist').set(180);
	                        robot.getJoint('wrist_rotate').set(200);
	                        robot.getJoint('wrist_rotate2').set(350);
	                         
			else:
				robot.getJoint('wrist_rotate').setSpeed(0);"""
	
		
if __name__=='__main__':
	main()
