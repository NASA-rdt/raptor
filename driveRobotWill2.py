import usb.core as usbdev
from legopi.lib.Adafruit_PWM_Servo_Driver import PWM
from legopi.lib import xbox_read
import time, thread

# Product information for the arm
pwm = PWM(0x40, debug=True)

DEADZONE=15000

# Timeout for our instructions through pyusb
TIMEOUT = 1000

class Joint:
	def __init__(self, channel, name, minVal, maxVal, defVal = 0):
                self.channel = channel;
		self.name = name;
		self.minVal = minVal;
		self.maxVal = maxVal;
		self.defVal = defVal;
		self.currentVal = defVal;
		self.speed = 0;
		self.changed=True;
	def setSpeed(self, speed):
		self.speed = speed;
	def toString(self):
		return "Joint('%s')=%d @ %d" % (self.name,self.currentVal,self.speed);
	def set(self, value):
		if value > self.maxVal:
			value = self.maxVal;
		if value < self.minVal:
			value = self.minVal;
		self.currentVal = value;
		self.changed=True;
	def reset(self):
		self.set(defVal);
	def delta(self, inc):
                if inc != 0:
                        self.set(self.currentVal+inc);
	def write(self,val): 
                if self.changed:
                        print 'Writing',val,'to',self.name
                	pwm.setPWM(self.channel, 0, self.currentVal);
                        self.changed=False
                
	def update(self):
		#print 'Updating',self.name;
		self.delta(self.speed);
		self.write(self.currentVal);
class RobotArm:

	def __init__(self):
		self.joints = [];
	def addJoint( self, joint):
		self.joints.append(joint);
		return self.joints.index(joint);

	def setJoint( self, joint , value ):
		self.joints.get(joint).set(value);

	def getJoint(self, name ):
		try:
			index = int(name)
			if name < len(self.joints):
				return self.joints[index];
			return None
		except ValueError:
			for joint in self.joints:
				if joint.name == name:
					return joint;
			return None;#check for null
	def setChanged(self):
                self.changed=True;
	def update(self):
                for joint in self.joints:
                        joint.update();
			
def run( robot, delay):
        running = True;
        while running:
                time.sleep(delay);
                robot.update();


robot = RobotArm();#this is the robot

#CREATE THE JOINTS HERE
        #Joint ( channel , name, min, max, default)
gripper = Joint(8, 'gripper',200,500,200);
wrist = Joint(6, 'wrist',160,500,330);
wrist_rotate = Joint(7, 'wrist_rotate',150,500,325);
wrist_rotate2 = Joint(5, 'wrist_rotate2',125,500,312);
elbow2 = Joint(4, 'elbow2',120,500,310);
elbow = Joint(3, 'elbow',125,500,312);
shoulder = Joint(2, 'shoulder',150,500,325);
base = Joint(0, 'base',150,500,325);


#ADD THE JOINTS BELOW:
robot.addJoint(base);
robot.addJoint(shoulder);
robot.addJoint(elbow);
robot.addJoint(elbow2);
robot.addJoint(wrist);
robot.addJoint(gripper);
robot.addJoint(wrist_rotate);
robot.addJoint(wrist_rotate2);

#Grip doesn't move at start

#this will get xbox commands
thread.start_new_thread( run, (robot,0.05));
for event in xbox_read.event_stream(deadzone = DEADZONE):
	#print "Xbox event: %s" % (event);
	
	if event.key == 'X1':
		if event.value > DEADZONE:
			robot.getJoint('base').setSpeed(-8);

		elif event.value < -DEADZONE:
			robot.getJoint('base').setSpeed(8);
			#print "setting speed -3"
		else:
			robot.getJoint('base').setSpeed(0);

	if event.key == 'Y1':
		if event.value > DEADZONE:
			robot.getJoint('shoulder').setSpeed(-6);

		elif event.value < -DEADZONE:
			robot.getJoint('shoulder').setSpeed(6);
			#print "setting speed -3"
		else:
			robot.getJoint('shoulder').setSpeed(0);
	
	if event.key == 'X2':
		if event.value > DEADZONE:
			robot.getJoint('wrist_rotate2').setSpeed(6);

		elif event.value < -DEADZONE:
			robot.getJoint('wrist_rotate2').setSpeed(-6);
			#print "setting speed -3"
		else:
			robot.getJoint('wrist_rotate2').setSpeed(0);

	if event.key == 'Y2':
		if event.value > DEADZONE:
			robot.getJoint('elbow').setSpeed(6);

		elif event.value < -DEADZONE:
			robot.getJoint('elbow').setSpeed(-6);
			#print "setting speed -3"
		else:
			robot.getJoint('elbow').setSpeed(0);

	if event.key == 'LB':
		if event.value == 1:
			robot.getJoint('elbow2').setSpeed(6);

		else:
			robot.getJoint('elbow2').setSpeed(0);

	if event.key == 'RB':
		if event.value == 1:
			robot.getJoint('elbow2').setSpeed(-6);

		else:
			robot.getJoint('elbow2').setSpeed(0);

	if event.key == 'LT':
		if event.value > 150:
			robot.getJoint('gripper').setSpeed(-9);

		else:
			robot.getJoint('gripper').setSpeed(0);

	if event.key == 'RT':
		if event.value > 150:
			robot.getJoint('gripper').setSpeed(9);

		else:
			robot.getJoint('gripper').setSpeed(0);

	if event.key == 'du':
		if event.value == 1:
			robot.getJoint('wrist').setSpeed(-6);

		else:
			robot.getJoint('wrist').setSpeed(0);

	if event.key == 'dd':
		if event.value == 1:
			robot.getJoint('wrist').setSpeed(6);

		else:
			robot.getJoint('wrist').setSpeed(0);

	if event.key == 'dr':
		if event.value == 1:
			robot.getJoint('wrist_rotate').setSpeed(6);

		else:
			robot.getJoint('wrist_rotate').setSpeed(0);

	if event.key == 'dl':
		if event.value == 1:
			robot.getJoint('wrist_rotate').setSpeed(-6);

		else:
			robot.getJoint('wrist_rotate').setSpeed(0);

	if event.key == 'dl':
		if event.value == 1:
			robot.getJoint('wrist_rotate').setSpeed(-6);

		else:
			robot.getJoint('wrist_rotate').setSpeed(0);

	
        if event.key == 'X':
                if event.value == 1:
                        robot.getJoint('shoulder').set(300);
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
			robot.getJoint('wrist_rotate').setSpeed(0);
        
        

        
        

        

#	elif ...other commands...
#

#Some other useful commands:
#print robot.joints;
#print robot.getJoint("wrist").name;
#print robot.getJoint(0).toString();
#robot.update();
#robot.getJoint('elbow').set(232)
#robot.update()

	
