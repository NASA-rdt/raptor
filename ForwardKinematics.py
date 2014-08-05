import numpy as np
import math as m
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt




#prints out end effector position given 7 dimensional array with radian values for motor positions
#as defined by DH parameters
def FK(angles,plot=0):
	#building other dh parameters
	theta = np.empty([8,1])
	for i in range (0,6):
		theta[i] = angles[i]
	theta[7] = 0
	alpha = [0, -np.pi/2, 0, 0, np.pi/2, -np.pi/2, np.pi/2, 0]
	a = [0, 0, 3.16, 1.7, 0, 0, 0, 0]
	d = [0, 0, 0, 0, 5.5, 0, 0, 5.5]

	#building transformation matricies
	T1=np.empty([4,4])
	T2=np.empty([4,4])
	T3=np.empty([4,4])
	T4=np.empty([4,4])
	T5=np.empty([4,4])
	T6=np.empty([4,4])
	T7=np.empty([4,4])
	T8=np.empty([4,4])


	i=0
	T1[0, 0] =  np.cos(theta[i])
	T1[0, 1] = -np.sin(theta[i])
	T1[0, 2] =  0
	T1[0, 3] =  a[i]
	T1[1, 0] =  np.sin(theta[i]) * np.cos(alpha[i])
	T1[1, 1] =  np.cos(theta[i]) * np.cos(alpha[i])
	T1[1, 2] = -np.sin(alpha[i])
	T1[1, 3] = -np.sin(alpha[i]) * d[i]
	T1[2, 0] =  np.sin(theta[i]) * np.sin(alpha[i])
	T1[2, 1] =  np.cos(theta[i]) * np.sin(alpha[i])
	T1[2, 2] =  np.cos(alpha[i])
	T1[2, 3] =  np.cos(alpha[i]) * d[i]
	T1[3, 0] =  0
	T1[3, 1] =  0
	T1[3, 2] =  0
	T1[3, 3] =  1
	


	i=1
	T2[0, 0] = np.cos(theta[i])
	T2[0, 1] =-np.sin(theta[i])
	T2[0, 2] = 0
	T2[0, 3] = a[i]
	T2[1, 0] = np.sin(theta[i]) * np.cos(alpha[i])
	T2[1, 1] = np.cos(theta[i]) * np.cos(alpha[i])
	T2[1, 2] = -np.sin(alpha[i])
	T2[1, 3] = -np.sin(alpha[i]) * d[i]
	T2[2, 0] = np.sin(theta[i]) * np.sin(alpha[i])
	T2[2, 1] = np.cos(theta[i]) * np.sin(alpha[i])
	T2[2, 2] = np.cos(alpha[i])
	T2[2, 3] = np.cos(alpha[i]) * d[i]
	T2[3, 0] = 0
	T2[3, 1] = 0
	T2[3, 2] = 0
	T2[3, 3] = 1

	i=2
	T3[0, 0] = np.cos(theta[i])
	T3[0, 1] =-np.sin(theta[i])
	T3[0, 2] = 0
	T3[0, 3] = a[i]
	T3[1, 0] = np.sin(theta[i]) * np.cos(alpha[i])
	T3[1, 1] = np.cos(theta[i]) * np.cos(alpha[i])
	T3[1, 2] = -np.sin(alpha[i])
	T3[1, 3] = -np.sin(alpha[i]) * d[i]
	T3[2, 0] = np.sin(theta[i]) * np.sin(alpha[i])
	T3[2, 1] = np.cos(theta[i]) * np.sin(alpha[i])
	T3[2, 2] = np.cos(alpha[i])
	T3[2, 3] = np.cos(alpha[i]) * d[i]
	T3[3, 0] = 0
	T3[3, 1] = 0
	T3[3, 2] = 0
	T3[3, 3] = 1


	i=3
	T4[0, 0] = np.cos(theta[i])
	T4[0, 1] =-np.sin(theta[i])
	T4[0, 2] = 0
	T4[0, 3] = a[i]
	T4[1, 0] = np.sin(theta[i]) * np.cos(alpha[i])
	T4[1, 1] = np.cos(theta[i]) * np.cos(alpha[i])
	T4[1, 2] = -np.sin(alpha[i])
	T4[1, 3] = -np.sin(alpha[i]) * d[i]
	T4[2, 0] = np.sin(theta[i]) * np.sin(alpha[i])
	T4[2, 1] = np.cos(theta[i]) * np.sin(alpha[i])
	T4[2, 2] = np.cos(alpha[i])
	T4[2, 3] = np.cos(alpha[i]) * d[i]
	T4[3, 0] = 0
	T4[3, 1] = 0
	T4[3, 2] = 0
	T4[3, 3] = 1


	i=4
	T5[0, 0] = np.cos(theta[i])
	T5[0, 1] =-np.sin(theta[i])
	T5[0, 2] = 0
	T5[0, 3] = a[i]
	T5[1, 0] = np.sin(theta[i]) * np.cos(alpha[i])
	T5[1, 1] = np.cos(theta[i]) * np.cos(alpha[i])
	T5[1, 2] = -np.sin(alpha[i])
	T5[1, 3] = -np.sin(alpha[i]) * d[i]
	T5[2, 0] = np.sin(theta[i]) * np.sin(alpha[i])
	T5[2, 1] = np.cos(theta[i]) * np.sin(alpha[i])
	T5[2, 2] = np.cos(alpha[i])
	T5[2, 3] = np.cos(alpha[i]) * d[i]
	T5[3, 0] = 0
	T5[3, 1] = 0
	T5[3, 2] = 0
	T5[3, 3] = 1
	

	i=5
	T6[0, 0] = np.cos(theta[i])
	T6[0, 1] =-np.sin(theta[i])
	T6[0, 2] = 0
	T6[0, 3] = a[i]
	T6[1, 0] = np.sin(theta[i]) * np.cos(alpha[i])
	T6[1, 1] = np.cos(theta[i]) * np.cos(alpha[i])
	T6[1, 2] = -np.sin(alpha[i])
	T6[1, 3] = -np.sin(alpha[i]) * d[i]
	T6[2, 0] = np.sin(theta[i]) * np.sin(alpha[i])
	T6[2, 1] = np.cos(theta[i]) * np.sin(alpha[i])
	T6[2, 2] = np.cos(alpha[i])
	T6[2, 3] = np.cos(alpha[i]) * d[i]
	T6[3, 0] = 0
	T6[3, 1] = 0
	T6[3, 2] = 0
	T6[3, 3] = 1
	

	i=6
	T7[0, 0] = np.cos(theta[i])
	T7[0, 1] =-np.sin(theta[i])
	T7[0, 2] = 0
	T7[0, 3] = a[i]
	T7[1, 0] = np.sin(theta[i]) * np.cos(alpha[i])
	T7[1, 1] = np.cos(theta[i]) * np.cos(alpha[i])
	T7[1, 2] = -np.sin(alpha[i])
	T7[1, 3] = -np.sin(alpha[i]) * d[i]
	T7[2, 0] = np.sin(theta[i]) * np.sin(alpha[i])
	T7[2, 1] = np.cos(theta[i]) * np.sin(alpha[i])
	T7[2, 2] = np.cos(alpha[i])
	T7[2, 3] = np.cos(alpha[i]) * d[i]
	T7[3, 0] = 0
	T7[3, 1] = 0
	T7[3, 2] = 0
	T7[3, 3] = 1


	i=7
	T8[0, 0] = np.cos(theta[i])
	T8[0, 1] =-np.sin(theta[i])
	T8[0, 2] = 0
	T8[0, 3] = a[i]
	T8[1, 0] = np.sin(theta[i]) * np.cos(alpha[i])
	T8[1, 1] = np.cos(theta[i]) * np.cos(alpha[i])
	T8[1, 2] = -np.sin(alpha[i])
	T8[1, 3] = -np.sin(alpha[i]) * d[i]
	T8[2, 0] = np.sin(theta[i]) * np.sin(alpha[i])
	T8[2, 1] = np.cos(theta[i]) * np.sin(alpha[i])
	T8[2, 2] = np.cos(alpha[i])
	T8[2, 3] = np.cos(alpha[i]) * d[i]
	T8[3, 0] = 0
	T8[3, 1] = 0
	T8[3, 2] = 0
	T8[3, 3] = 1



	P1 = T1
	P2 = np.dot(P1,T2)
	P3 = np.dot(P2,T3)
	P4 = np.dot(P3,T4)
	P5 = np.dot(P4,T5)
	P6 = np.dot(P5,T6)
	P7 = np.dot(P6,T7)
	P8 = np.dot(P7,T8)

	position = np.empty([3,8])

	position[0, 0] = P1[0,3]
	position[1, 0] = P1[1,3]
	position[2, 0] = P1[2,3]

	position[0, 1] = P2[0,3]
	position[1, 1] = P2[1,3]
	position[2, 1] = P2[2,3]

	position[0, 2] = P3[0,3]
	position[1, 2] = P3[1,3]
	position[2, 2] = P3[2,3]

	position[0, 3] = P4[0,3]
	position[1, 3] = P4[1,3]
	position[2, 3] = P4[2,3]

	position[0, 4] = P5[0,3]
	position[1, 4] = P5[1,3]
	position[2, 4] = P5[2,3]

	position[0, 5] = P6[0,3]
	position[1, 5] = P6[1,3]
	position[2, 5] = P6[2,3]

	position[0, 6] = P7[0,3]
	position[1, 6] = P7[1,3]
	position[2, 6] = P7[2,3]

	position[0, 7] = P8[0,3]
	position[1, 7] = P8[1,3]
	position[2, 7] = P8[2,3]


	#for j in range (0,2):
	#	position[j,0] = P8[j, 3]


	if plot == 1:
		mpl.rcParams['legend.fontsize'] = 10
		fig = plt.figure(1)
		ax = fig.gca(projection = '3d')

		x = []
		y = []
		z = []
		for i in range (0, 8):
			x.append(position[0,i])
			y.append(position[1,i])
			z.append(position[2,i])
		ax.plot(x,y,z,label='Robot Arm')
		ax.legend()
		plt.show(block = False)


	return position[:,7]