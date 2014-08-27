# Example file for testing the OWI Robotic Arm
# For use with RobotArm.py
#
# (C) Matt Dyson 2013
# http://mattdyson.org/projects/robotarm

import RobotArm
import time

arm = RobotArm.RobotArm()

print "Moving elbow"
arm.moveElbow(100)
time.sleep(1)

print "Moving wrist as well"
arm.moveWrist(100)
time.sleep(1)

print "Moving base as well"
arm.moveBase(200)
time.sleep(3)



"""print "Moving elbow back"
arm.moveElbow(200)
time.sleep(1)

print "Moving wrist back as well"
arm.moveWrist(200)
time.sleep(1)

print "Moving base back as well"
arm.moveBase(100)
time.sleep(3)"""

