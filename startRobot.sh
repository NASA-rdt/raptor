#!/bin/bash

sudo python /home/pi/RobotArm/lightcontrol/controllerUSBStatus.py &
sudo python /home/pi/RobotArm/SpaceNavControl.py &
sudo python /home/pi/RobotArm/driveRobotMapped.py &

exit 0
