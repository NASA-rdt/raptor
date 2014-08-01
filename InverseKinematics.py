import numpy as np
import math as m
import scipy.sparse.linalg as linalg


#a wrapper to turn ugly into pretty, 
#'from' is current joint angles, 'delta' is expected changes, 'which method' tells what to use. 
#optional:
#0 = damped least square (default), 1 = old method
#damp is damped least square dampening coefficient, default is 0
def goTo( _from, delta,whichmethod = 0, damp = 0.0):
    if whichmethod == 0:
        return DLSqr(_from, delta, damp)

    else:
		return FullIK(_from[0],_from[1],_from[2],_from[3],_from[4],_from[5],_from[6],delta[0],delta[1],delta[2],delta[3],delta[4],delta[5])




####use FullIK for the actual inverse kinematics.
#th1-7 are current angles (radians)
#delta_ are wanted changes of endeffector (x, y, z positions (inches), roll, pitch, yaw angles (radians))	
def FullIK(th1,th2,th3,th4,th5,th6,th7,deltax,deltay,deltaz,deltar,deltap,deltaw):
    DelAngles = IK(th1, th2, th3, th4, th5, th6, th7, deltax, deltay, deltaz, deltar, deltap, deltaw)
    new = NewAngles(th1, th2, th3, th4, th5, th6, th7, DelAngles)
    return new


def IK(th1, th2, th3, th4, th5, th6, th7, deltax, deltay, deltaz, deltar, deltap, deltaw):
    J = jacbuild(th1, th2, th3, th4, th5, th6, th7)

    Deltas = np.empty([6, 1])
    Deltas[0, 0] = deltax
    Deltas[1, 0] = deltay
    Deltas[2, 0] = deltaz
    Deltas[3, 0] = deltar
    Deltas[4, 0] = deltap
    Deltas[5, 0] = deltaw
    InvJ = np.linalg.pinv(J)
    DelAngles = np.dot(InvJ, Deltas)
    return DelAngles


def NewAngles(th1, th2, th3, th4, th5, th6, th7, DelAngles):
    new = np.empty([7, 1])
    new[0] = th1 + DelAngles[0]
    new[1] = th2 + DelAngles[1]
    new[2] = th3 + DelAngles[2]
    new[3] = th4 + DelAngles[3]
    new[4] = th5 + DelAngles[4]
    new[5] = th6 + DelAngles[5]
    new[6] = th7 + DelAngles[6]
    return new


def DLSqr(theta, delta, damp = 0.0):
    J = jacbuild(theta[0], theta[1], theta[2], theta[3], theta[4], theta[5], theta[6])
    DT = linalg.lsqr(J, delta, damp)
    DelAngles = DT[1]
    new = NewAngles(theta[0], theta[1], theta[2], theta[3], theta[4], theta[5], theta[6],DelAngles)
    return new


def jacbuild(th1=0.2, th2=-1.3, th3=0.8, th4=1.2, th5=-0.6, th6=1.9, th7=-0.8, show=0):
    #preset angles are for testing
    #all angles are in radians
    #builds the jacobian matrix
    #define link lengths
    a2 = 3.16
    a3 = 1.7
    d5 = 5.5
    zt = 5.5
    #initialize
    J = np.empty([6, 7])
    #build entry-by-entry
    J[0, 0] = (- m.cos(th2) * m.sin(th1) * a2) \
    - m.cos(th2 + th3) * m.sin(th1) * a3 \
    - m.sin(th1) * m.sin(th2 + th3 + th4) * d5 \
    - m.cos(th6) * m.sin(th1) * m.sin(th2 + th3 + th4) * zt \
    - m.cos(th2 + th3 + th4) * m.cos(th5) * m.sin(th1) * m.sin(th6) * zt \
    - m.cos(th1) * m.sin(th5) * m.sin(th6) * zt

    J[0, 1] = - m.cos(th1) * (m.sin(th2) * a2 \
    + m.sin(th2 + th3) * a3 - m.cos(th2 + th3 + th4) * d5 \
    - m.cos(th2 + th3 + th4) * m.cos(th6) * zt \
    + m.cos(th5) * m.sin(th2 + th3 + th4) * m.sin(th6) * zt)

    J[0, 2] = m.cos(th1) * (- m.sin(th2 + th3) * a3 + m.cos(th2 + th3 + th4) * d5 \
    + (m.cos(th2 + th3 + th4) * m.cos(th6) - m.cos(th5) * m.sin(th2 + th3 + th4) * m.sin(th6)) * zt)

    J[0, 3] = m.cos(th1) * (m.cos(th2 + th3 + th4) * d5 + \
    (m.cos(th2 + th3 + th4) * m.cos(th6) - m.cos(th5) * m.sin(th2 + th3 + th4) * m.sin(th6)) * zt)

    J[0, 4] = -(m.cos(th5) * m.sin(th1) + m.cos(th1) * m.cos(th2 + th3 + th4) * m.sin(th5)) * m.sin(th6) * zt

    J[0, 5] = (-m.cos(th6) * m.sin(th1) * m.sin(th5) \
    + m.cos(th1) * (m.cos(th2 + th3 + th4) * m.cos(th5) * m.cos(th6) \
    - m.sin(th2 + th3 + th4) * m.sin(th6))) * zt

    J[0, 6] = 0

    J[1, 0] = m.cos(th1) * m.cos(th2) *a2 + m.cos(th1) * m.cos(th2+th3) * a3 \
    + m.cos(th1) * m.sin(th2 + th3 +th4) *d5 \
    + m.cos(th1) * m.cos(th6) * m.sin(th2+th3+th4) *zt \
    + m.cos(th1) * m.cos(th2 + th3 + th4) * m.cos(th5) * m.sin(th6) * zt \
    - m.sin(th1) * m.sin(th5) * m.sin(th6) *zt

    J[1, 1] = - m.sin(th1) * (m.sin(th2) * a2 + m.sin(th2 + th3)*a3 -m.cos(th2 + th3 + th4) * d5 \
    - m.cos(th2 + th3 + th4) * m.cos(th6) * zt + m.cos(th5) * m.sin(th2 + th3 + th4) * m.sin(th6) * zt)

    J[1, 2] = m.sin(th1) * (- m.sin(th2 + th3) * a3 + m.cos(th2 + th3 + th4) * d5 \
    + (m.cos(th2 + th3 + th4) * m.cos(th6) - m.cos(th5) * m.sin(th2 +th3 + th4) * m.sin(th6)) * zt)

    J[1, 3] = m.sin(th1) * (m.cos(th2 + th3 + th4) * d5 + \
    (m.cos(th2 + th3 + th4) * m.cos(th6) - m.cos(th5) * m.sin(th2 + th3 + th4) * m.sin(th6)) * zt)

    J[1, 4] = (m.cos(th1) * m.cos(th5) - m.cos(th2 + th3 + th4) * m.sin(th1) * m.sin(th5))*m.sin(th6) *zt

    J[1, 5] =  (m.cos(th2 +th3 + th4) * m.cos(th5) *m.cos(th6)*m.sin(th1) + \
    m.cos(th1) * m.cos(th6) * m.sin(th5) - \
    m.sin(th1) * m.sin(th2 + th3 + th4) * m.sin(th6)) * zt

    J[1, 6] = 0

    J[2, 0] = 0

    J[2, 1] = (-4 * m.cos(th2) * a2 - 4 * m.cos(th2 + th3) * a3 - \
    4 * m.sin(th2 + th3 + th4) * d5 - 2 * m.sin(th2 + th3 + th4 - th6) * zt + \
    m.sin(th2 + th3 + th4 - th5 - th6) * zt + m.sin(th2 + th3 + th4 +th5 -th6) * zt - \
    2 * m.sin(th2 + th3 + th4 + th6) * zt - m.sin(th2 + th3 + th4 - th5 + th6) * zt - \
    m.sin(th2 + th3 + th4 + th5 + th6) * zt) / 4

    J[2, 2] = (-4 * m.cos(th2 + th3) * a3 - 4 * m.sin(th2 + th3 + th4) * d5 - \
    (2 * m.sin(th2 + th3 + th4 - th6) - m.sin(th2 + th3 + th4 - th5 - th6) - \
    m.sin(th2 + th3 + th4 + th5 - th6) + 2* m.sin(th2 + th3 + th4 + th6) + \
    m.sin(th2 + th3 + th4 - th5 + th6) + m.sin(th2 + th3 + th4 + th5 + th6)) * zt) / 4

    J[2, 3] = (-4 * m.sin(th2 + th3 + th4) * d5 - \
    (2 * m.sin(th2 + th3 + th4 - th6) - m.sin(th2 + th3 + th4 - th5 - th6) - \
    m.sin(th2 + th3 + th4 + th5 - th6) + 2 * m.sin(th2 + th3 + th4 + th6) + \
    m.sin(th2 + th3 + th4 - th5 + th6) + m.sin(th2 + th3 + th4 + th5 + th6)) * zt) / 4

    J[2, 4] = m.sin(th2 + th3 + th4) * m.sin(th5) * m.sin(th6) * zt

    J[2, 5] = -1 * ((-2 * m.sin(th2 + th3 + th4 -th6) + \
    m.sin(th2 + th3 + th4 - th5 - th6) + m.sin(th2 + th3 + th4 + th5 - th6) +\
    2 * m.sin(th2 + th3 + th4 + th6) + m.sin(th2 + th3 + th4 - th5 + th6) + \
    m.sin(th2 + th3 + th4 + th5 + th6)) * zt) / 4

    J[2, 6] = 0

    J[3, 0] = 0
    J[3, 1] = - m.sin(th1)
    J[3, 2] = - m.sin(th1)
    J[3, 3] = - m.sin(th1)
    J[3, 4] = m.cos(th1) * m.sin(th2 + th3 + th4)
    J[3, 5] = - m.cos(th5) * m.sin(th1) - m.cos(th1) * m.cos(th2 + th3 + th4) * m.sin(th5)
    J[3, 6] = -m.sin(th1) * m.sin(th5) * m.sin(th6) + \
    m.cos(th1) * (m.cos(th6) * m.sin(th2 + th3 + th4) + \
    m.cos(th2 + th3 + th4) * m.cos(th5) * m.sin(th6))

    J[4, 0] = 0
    J[4, 1] = m.cos(th1)
    J[4, 2] = m.cos(th1)
    J[4, 3] = m.cos(th1)
    J[4, 4] = m.sin(th1) * m.sin(th2 + th3 + th4)
    J[4, 5] = m.cos(th1) * m.cos(th5) - m.cos(th2 + th3 + th4) * m.sin(th1) * m.sin(th5)
    J[4, 6] = m.cos(th6) * m.sin(th1) * m.sin(th2 + th3 + th4) + \
    (m.cos(th2 + th3 + th4) * m.cos(th5) * m.sin(th1) + m.cos(th1) * m.sin(th5)) * m.sin(th6)
    J[5, 0] = 1
    J[5, 1] = 0
    J[5, 2] = 0
    J[5, 3] = 0
    J[5, 4] = m.cos(th2 + th3 + th4)
    J[5, 5] = m.sin(th2 + th3 + th4) * m.sin(th5)
    J[5, 6] = (2 * m.cos(th2 + th3 + th4 - th6) - \
    m.cos(th2 + th3 + th4 - th5 - th6) - m.cos(th2+th3+th4+th5-th6) + \
    2 * m.cos(th2 + th3 + th4 + th6) + m.cos(th2 + th3 + th4 - th5 + th6) + \
    m.cos(th2 + th3 + th4 + th5 + th6)) / 4

    if show == 1:
        print J
    return J


