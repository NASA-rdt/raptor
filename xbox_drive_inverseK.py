#!/usr/bin/python
from driveRobotWill2 import RobotArm,Joint

DEADZONE=15000

#def main():
	robot = RobotArm();#this is the robot
	
	#CREATE THE JOINTS HERE
	         #Joint ( channel , name, min, max, default) 
	gripper = Joint(8, 'gripper',120,400,300);   #BLANK
	wrist = Joint(6, 'wrist',120,500,415);  #Y/P
	wrist_rotate2 = Joint(7, 'wrist_rotate2',170,490,240);  #B/P
	wrist_rotate = Joint(5, 'wrist_rotate',125,500,312);  #5
	elbow2 = Joint(4, 'elbow2',120,500,330);   #B/Y
	elbow = Joint(3, 'elbow',125,500,230);  #P
	shoulder = Joint(2, 'shoulder',200,500,340);  #B
	base = Joint(0, 'base',150,500,300);  #Y
	
	
	#ADD THE JOINTS BELOW:
	robot.addJoint(base);
	robot.addJoint(shoulder);
	robot.addJoint(elbow);
	robot.addJoint(elbow2);
	robot.addJoint(wrist);
	robot.addJoint(gripper);
	robot.addJoint(wrist_rotate);    
	
	robot.addJoint(wrist_rotate2);

        print 'Robot Arm Ready..'

	try:
		while True:
			#
		






	except KeyboardInterrupt:
		print '\nQuitting...'
	finally:

print '*NOT* moving robot...'
	#if(inverseKinematics):
	deltas = (0,0,0,0,0,0)
	robot.goToXYZ( deltas )

	
        print '**now** moving robot...'
	deltas = (1,0,0,0,0,0)
	robot.goToXYZ( deltas )

        print '**now** AT position: ',
        robot.getCurrentPose()
	
	#this will get xbox commands
	input('ready?')
	
#if __name__=='__main__':
#	main()
