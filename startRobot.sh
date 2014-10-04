#!/bin/bash

(sudo xboxdrv -d -D -v --dbus disabled) &
sleep 5
sudo python /home/pi/RobotArm/SpaceNavControl.py &
sudo python /home/pi/RobotArm/lightcontrol/controllerUSBStatus.py &
sudo python /home/pi/RobotArm/driveRobotMapped.py &
