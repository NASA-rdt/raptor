import time
import cwiid
from Wiimote import connect
from legopi.lib.Adafruit_PWM_Servo_Driver import PWM
from driveRobotWill2 import Joint, RobotArm
print "up here"
pwm = PWM(0x40, debug=True)
pwm.setPWMFreq(60)
print "something1" 
robot = RobotArm();#this is the robot
print "something2" 
#CREATE THE JOINTS HERE
        #Joint ( channel , name, min, max, default) 
gripper = Joint(8, 'gripper',120,400,300);   #BLANK
wrist = Joint(6, 'wrist',120,500,310);  #Y/P
wrist_rotate2 = Joint(7, 'wrist_rotate2',170,490,330);  #B/P
wrist_rotate = Joint(5, 'wrist_rotate',125,500,312);  #5
elbow2 = Joint(4, 'elbow2',120,500,250);   #B/Y
elbow = Joint(3, 'elbow',125,500,300);  #P
shoulder = Joint(2, 'shoulder',200,500,300);  #B
base = Joint(0, 'base',150,500,325);  #Y


#ADD THE JOINTS BELOW:
robot.addJoint(base);
robot.addJoint(shoulder);
robot.addJoint(elbow);
robot.addJoint(elbow2);
robot.addJoint(wrist);
robot.addJoint(gripper);
robot.addJoint(wrist_rotate);    
robot.addJoint(wrist_rotate2);

print "attempting to connect to wiimote"
wm = connect()
wiiRoll = 0 
wiiPitch = 0
print "test"

while True:
	wiiRoll = wm.state['acc'][0]
	#print wiiRoll
	wiiPitch = wm.state['acc'][1]
	#print wiiPitch
	if (wm.state['buttons'] & cwiid.BTN_B):
		if wiiRoll < 105:
			robot.getJoint('wrist').setSpeed(6);
		elif wiiRoll > 135:
			robot.getJoint('wrist').setSpeed(-6);
		elif wiiPitch < 115:
			robot.getJoint('wrist_rotate').setSpeed(-6);
		elif wiiPitch > 130:
			robot.getJoint('wrist_rotate').setSpeed(6);
		else:
			robot.getJoint('wrist_rotate').setSpeed(0);
			robot.getJoint('wrist').setSpeed(0);
	else:
		robot.getJoint('wrist_rotate').setSpeed(0);
		robot.getJoint('wrist').setSpeed(0);
	if (wm.state['buttons'] & cwiid.BTN_A):
		if wiiRoll < 105:
			robot.getJoint('elbow2').setSpeed(6);
		elif wiiRoll > 135:
			robot.getJoint('elbow2').setSpeed(-6);
		elif wiiPitch < 115:
			robot.getJoint('wrist_rotate2').setSpeed(-6);
		elif wiiPitch > 130:
			robot.getJoint('wrist_rotate2').setSpeed(6);
		else:
			robot.getJoint('wrist_rotate2').setSpeed(0);
			robot.getJoint('elbow2').setSpeed(0);
	else:
		robot.getJoint('wrist_rotate2').setSpeed(0);
		robot.getJoint('elbow2').setSpeed(0);
	if (wm.state['buttons'] & cwiid.BTN_DOWN):
                #print "buttz"
		robot.getJoint('base').setSpeed(-6);
	elif (wm.state['buttons'] & cwiid.BTN_UP):
                #print "buttz1"
		robot.getJoint('base').setSpeed(6);
	else:
		robot.getJoint('base').setSpeed(0);
	if (wm.state['buttons'] & cwiid.BTN_LEFT):
                #print "buttz2"
		robot.getJoint('shoulder').setSpeed(-6);
	elif (wm.state['buttons'] & cwiid.BTN_RIGHT):
                #print "buttz3"
		robot.getJoint('shoulder').setSpeed(6);
	else:
		robot.getJoint('shoulder').setSpeed(0);
	if (wm.state['buttons'] & cwiid.BTN_1):
                #print "buttz4"
		robot.getJoint('gripper').setSpeed(-6);
	elif (wm.state['buttons'] & cwiid.BTN_2):
                #print "buttz5"
		robot.getJoint('gripper').setSpeed(6);
	else:
		robot.getJoint('gripper').setSpeed(0);
	if (wm.state['buttons'] & cwiid.BTN_MINUS):
                #print "buttz6"
		robot.getJoint('elbow').setSpeed(6);
	elif (wm.state['buttons'] & cwiid.BTN_PLUS):
                #print "buttz7"
		robot.getJoint('elbow').setSpeed(-6);
	else:
		robot.getJoint('elbow').setSpeed(0);
