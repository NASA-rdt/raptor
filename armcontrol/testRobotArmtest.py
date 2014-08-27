# Example file for testing the OWI Robotic Arm
# For use with RobotArm.py
#
# (C) Matt Dyson 2013
# http://mattdyson.org/projects/robotarm

import RobotArm
import time

arm = RobotArm.RobotArm()

print "Moving grip"
arm.moveShoulder(-100)
time.sleep(3)

print "Moving grip again"
arm.moveShoulder(100)
time.sleep(3)


