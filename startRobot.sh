#!/bin/bash

sudo python /home/pi/RobotArm/SpaceNavControl.py &

sleep 10
sudo python /home/pi/RobotArm/lightcontrol/controllerUSBStatus.py &
sudo python /home/pi/RobotArm/driveRobotMapped.py &
