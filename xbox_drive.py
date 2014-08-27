#!/usr/bin/python
from driveRobotWill2 import RobotArm,Joint, xbox_read

DEADZONE=15000

def main():
	robot = RobotArm();#this is the robot
	
	#CREATE THE JOINTS HERE
	        #Joint ( channel , name, min, max, default) 
	gripper = Joint(8, 'gripper',120,400,400);   #BLANK
	wrist = Joint(6, 'wrist',120,680,320);  #Y/P
	wrist_rotate2 = Joint(7, 'wrist_rotate2',130,680,400);  #B/P
	wrist_rotate = Joint(5, 'wrist_rotate',125,680,400);  #5
	elbow2 = Joint(4, 'elbow2',120,680,400);   #B/Y
	elbow = Joint(3, 'elbow',120,680,400);  #P
	shoulder = Joint(2, 'shoulder',200,680,400);  #B
	base = Joint(0, 'base',120,680,400);  #Y
	
	
	#ADD THE JOINTS BELOW:
	robot.addJoint(base);
	robot.addJoint(shoulder);
	robot.addJoint(elbow);
	robot.addJoint(elbow2);
	robot.addJoint(wrist);
	robot.addJoint(gripper);
	robot.addJoint(wrist_rotate);    
	
	robot.addJoint(wrist_rotate2);

	loop(robot)

def loop(robot):	
	for event in xbox_read.event_stream(deadzone = DEADZONE):
		#print "Xbox event: %s" % (event);
		
		if event.key == 'X1':
			if event.value > DEADZONE:
				robot.getJoint('base').setSpeed(-8);
				print "base ", robot.getJoint('base').currentVal

			elif event.value < -DEADZONE:
				robot.getJoint('base').setSpeed(8);
				print "base ", robot.getJoint('base').currentVal
			else:
				robot.getJoint('base').setSpeed(0);
				
		if event.key == 'Y1':
			if event.value > DEADZONE:
				robot.getJoint('shoulder').setSpeed(-6);
				print "shoulder ", robot.getJoint('shoulder').currentVal

			elif event.value < -DEADZONE:
				robot.getJoint('shoulder').setSpeed(6);
				print "shoulder ", robot.getJoint('shoulder').currentVal
			else:
				robot.getJoint('shoulder').setSpeed(0);
				
		if event.key == 'X2':
			if event.value > DEADZONE:
				robot.getJoint('wrist_rotate2').setSpeed(-6);
				print "Wrist rotate2 ", robot.getJoint('wrist_rotate2').currentVal

			elif event.value < -DEADZONE:
				robot.getJoint('wrist_rotate2').setSpeed(6);
				print "Wrist rotate2 ", robot.getJoint('wrist_rotate2').currentVal
			else:
				robot.getJoint('wrist_rotate2').setSpeed(0);
	
		if event.key == 'Y2':
			if event.value > DEADZONE:
				robot.getJoint('elbow').setSpeed(-6);
				print "elbow ", robot.getJoint('elbow').currentVal

			elif event.value < -DEADZONE:
				robot.getJoint('elbow').setSpeed(6);
				print "elbow ", robot.getJoint('elbow').currentVal

			else:
				robot.getJoint('elbow').setSpeed(0);
	
		if event.key == 'LB':
			if event.value == 1:
				robot.getJoint('elbow2').setSpeed(6);
				print "elbow 2 ", robot.getJoint('elbow2').currentVal

			else:
				robot.getJoint('elbow2').setSpeed(0);
	
		if event.key == 'RB':
			if event.value == 1:
				robot.getJoint('elbow2').setSpeed(-6);
				print "elbow 2 ", robot.getJoint('elbow2').currentVal

	
			else:
				robot.getJoint('elbow2').setSpeed(0);
	
		if event.key == 'LT':
			if event.value > 150:
				robot.getJoint('gripper').setSpeed(9);
				print "gripper ", robot.getJoint('gripper').currentVal
	
			else:
				robot.getJoint('gripper').setSpeed(0);
	
		if event.key == 'RT':
			if event.value > 150:
				robot.getJoint('gripper').setSpeed(-9);
				print "gripper ", robot.getJoint('gripper').currentVal

			else:
				robot.getJoint('gripper').setSpeed(0);
	
		if event.key == 'du':
			if event.value == 1:
				robot.getJoint('wrist').setSpeed(6);
				print "wrist ", robot.getJoint('wrist').currentVal

			else:
				robot.getJoint('wrist').setSpeed(0);
	
		if event.key == 'dd':
			if event.value == 1:
				robot.getJoint('wrist').setSpeed(-6);
				print "wrist ", robot.getJoint('shoulder').currentVal

			else:
				robot.getJoint('wrist').setSpeed(0);
	
		if event.key == 'dr':
			if event.value == 1:
				robot.getJoint('wrist_rotate').setSpeed(-6);
				print "wrist_rotate ", robot.getJoint('wrist_rotate').currentVal
	
			else:
				robot.getJoint('wrist_rotate').setSpeed(0);
	
		if event.key == 'dl':
			if event.value == 1:
				robot.getJoint('wrist_rotate').setSpeed(6);
				print "wrist_rotate ", robot.getJoint('wrist_rotate').currentVal
	
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
