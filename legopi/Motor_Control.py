#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x40, debug=True)
ch = 0
angle = 0
while(True):
	angle = input("What angles (in the format of a list e.g. [a,b,c,d,e,f])?")
	#print(angle)
	if angle[0]<106:
                angle[0]=106
        if angle[1]<106:
                angle[1]=106
        if angle[2]<106:
                angle[2]=106
        if angle[3]<106:
                angle[3]=106
        if angle[4]<1:
                angle[4]=1
        if angle[5]<1:
                angle[5]=1
        if angle[0]>683:
                angle[0]=683
        if angle[1]>686:
                angle[1]=686
        if angle[2]>689:
                angle[2]=689
        if angle[3]>686:
                angle[3]=686
        if angle[4]>530:
                angle[4]=530
        if angle[5]>580:
                angle[5]=580
        print(angle)

	"""pwm.setPWM(0, 0, angle[0])
	pwm.setPWM(2, 0, angle[1])
	pwm.setPWM(4, 0, angle[2])
	pwm.setPWM(6, 0, angle[3])
	pwm.setPWM(8, 0, angle[4])
	pwm.setPWM(10, 0, angle[5])"""



	"""angle1 = int(input("What angle?"))
	angle2 = int(input("What angle?"))
	angle3 = int(input("What angle?"))
	angle4 = int(input("What angle?"))
	angle5 = int(input("What angle?"))"""
	
