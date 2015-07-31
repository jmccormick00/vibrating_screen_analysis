__author__ = 'jrmccormick'

# Imports ======================================
import numpy as np
import scipy.integrate
from matplotlib import pyplot as plt

# Update Function ==============================
def screendynamics(state, t):
    X0 = state[0]
    dX0 = state[1]
    Y0 = state[2]
    dY0 = state[3]
    Theta0 = state[4]
    dTheta0 = state[5]
    X1 = state[6]
    dX1 = state[7]
    Y1 = state[8]
    dY1 = state[9]
    X2 = state[10]
    dX2 = state[11]
    Y2 = state[12]
    dY2 = state[13]
    X3 = state[14]
    dX3 = state[15]
    Y3 = state[16]
    dY3 = state[17]

    # Screen Constants ==================================
    # Screen Eccentric mass
    m0=683.2 #slugs
    # Screen moment of inertia
    J0=84153.8 #slugs*ft^2
    # Screen body angle
    alpha=-0.052 # radians
    # Spring Feed stiffness
    Sfx=32736 #16368 #lb/ft
    Sfy=32736 #lb/ft
    # Spring discharge stiffness
    Sdx=32736 #16368 #lb/ft
    Sdy=32736 #lb/ft
    # Feed Spring placement
    Xf=-9 #ft
    Yf=1 #ft
    # Discharge Spring placement
    Xd=8 #ft
    Yd=1 #ft
    # ===================================================

    # Mechanism Constants ===============================
    # Counterweight 1 & 3 mass
    m1=m3=1.5 #slugs
    # Starting Angle
    A1=A3=4.7124 #Radians
    # Counterweight 2 mass
    m2=1.5 #slugs
    # Lag Angle
    LA=1. # radians
    A2=A1-LA
    # Eccentric distance of mass
    r=0.5 # ft
    # angular velocity
    omega1=omega3=800*(2*np.pi)/60 #rad/sec
    omega2=-omega1
    # Bearing stiffness
    Kb=200e7 # lbf/ft
    # ===================================================

    ddX1=(m1*r*omega1*omega1*np.cos(A1+omega1*t)-Kb*X1)/m1
    ddY1=(m1*r*omega1*omega1*np.sin(A1+omega1*t)-Kb*Y1)/m1

    ddX2=(m2*r*omega2*omega2*np.cos(A2+omega2*t)-Kb*X2)/m2
    ddY2=(m2*r*omega2*omega2*np.sin(A2+omega2*t)-Kb*Y2)/m2

    ddX3=(m3*r*omega3*omega3*np.cos(A3+omega3*t)-Kb*X3)/m3
    ddY3=(m3*r*omega3*omega3*np.sin(A3+omega3*t)-Kb*Y3)/m3

    # Screen Adjusted Spring Stiffness
    Sfax=Sfy*np.sin(alpha)+Sfx*np.cos(alpha)
    Sfay=Sfy*np.cos(alpha)+Sfx*np.sin(alpha)
    Sdax=Sdy*np.sin(alpha)+Sdx*np.cos(alpha)
    Sday=Sdy*np.cos(alpha)+Sdx*np.sin(alpha)

    # Screen Spring deformation
    Dfx=X0+(Xf*np.cos(Theta0)-Yf*np.sin(Theta0))-Xf
    Dfy=Y0+(Xf*np.sin(Theta0)+Yf*np.cos(Theta0))-Yf
    Ddx=X0+(Xd*np.cos(Theta0)-Yd*np.sin(Theta0))-Xd
    Ddy=Y0+(Xd*np.sin(Theta0)+Yd*np.cos(Theta0))-Yd

    # Screen Equations of motion
    ddX0=((2*Kb*(X1+X2+X3))-(2*Sfax*Dfx)-(2*Sdax*Ddx))/m0
    ddY0=((2*Kb*(Y1+Y2+Y3))-(2*Sfay*Dfy)-(2*Sday*Ddy))/m0 - 32.2
    ddTheta0=((-Yd*2*Sdax*Ddx)+(Xd*2*Sday*Ddy)-(Yf*2*Sfax*Dfx)+(Xf*2*Sfay*Dfy))/J0

    return [dX0, ddX0, dY0, ddY0, dTheta0, ddTheta0, dX1, ddX1, dY1, ddY1, dX2, ddX2, dY2, ddY2, dX3, ddX3, dY3, ddY3]

dt=.001
end_t=5
state0=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
time = np.linspace(0, end_t, num=end_t/dt)
dynamics=scipy.integrate.odeint(screendynamics, state0, time)
x0=dynamics[:,0]
y0=dynamics[:,2]
theta0=dynamics[:,4]
x1=dynamics[:,6]
y1=dynamics[:,8]
x2=dynamics[:,10]
y2=dynamics[:,12]
x3=dynamics[:,14]
y3=dynamics[:,16]

xr=x1+x2+x3
yr=y1+y2+y3
Dr=np.sqrt((xr*xr)+(yr*yr))
Dtheta=np.arctan2(xr,yr)

fig=plt.figure(figsize=(20,7))
mPlot1=fig.add_subplot(131, axisbg='#d5de9c')
mPlot1.plot(time, theta0)

mPlot2=fig.add_subplot(132, axisbg='#d5de9c')
mPlot2.plot(time, y2)

mPlot3=fig.add_subplot(133, polar=True, axisbg='#d5de9c')
r=np.sqrt((x0*x0)+(y0*y0))
theta=np.arctan2(y0, x0)
mPlot3.plot(Dtheta, Dr)

plt.show()