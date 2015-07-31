__author__ = 'jrmccormick'

import mechanism
import numpy as np
from matplotlib import pyplot as plt

# Mechanism Parameters
Mech_weight=100 # lbs
Mech_centerWeight=100 # lbs
Mech_rpm=800 # rot/min
Mech_radius=0.5 # ft
Mech_lagAngle=90 # deg

# Screen Parameters
Screen_eccentricWeight=36000 # pounds

system=mechanism.MechanismSystem(weight=Mech_weight, centerWeight=Mech_centerWeight, rpm=Mech_rpm, radius=Mech_radius, lagAngle=Mech_lagAngle, screenWeight=Screen_eccentricWeight)
t = np.linspace(0.0, 1.0/Mech_rpm*60.0, num=300)
system.calculateForces(t)

fig=plt.figure(figsize=(20,7))
fig.suptitle("RPM:{:.2f} | Weight(1&3):{:.2f}(lbs) | Center Weight:{:.2f}(lbs) | Radius:{:.2f}(ft) | Lag Angle:{:.2f}(deg)"
             .format(Mech_rpm, Mech_weight, Mech_centerWeight, Mech_radius, Mech_lagAngle))

# Set up the resultant plot
polar=fig.add_subplot(131, polar=True, axisbg='#d5de9c')
polar.plot(system.theta, system.fr)
polar.set_title("Combined Throw Force(lbs)\nEllipse Angle:{:.2f}(deg)".format(np.rad2deg(system.resultAngle)), va='bottom')
polar.grid(True,which='major')
polar.set_xticks(np.pi/180*np.linspace(0,360,24,endpoint=False))

# Create the profile for CounterWeight 1
mPlot1=fig.add_subplot(132, polar=True, axisbg='#d5de9c')
max=np.max(system.m1.fr)
mPlot1.plot(system.m1.theta, system.m1.fr)
mPlot1.plot(system.m1.startAngle, max, 'ro', markersize=15)
mPlot1.set_rmax(1.2*max)
mPlot1.set_title("CounterWeight 1&3 Throw Force(lbs)\nCounter-Clockwise Rotation", va='bottom')
mPlot1.grid(True,which='major')
mPlot1.set_xticks(np.pi/180*np.linspace(0,360,24,endpoint=False))

# Create the profile for CounterWeight 2
mPlot2=fig.add_subplot(133, polar=True, axisbg='#d5de9c')
max=np.max(system.m2.fr)
mPlot2.plot(system.m2.theta, system.m2.fr)
mPlot2.plot(system.m2.startAngle, max, 'ro', markersize=15)
mPlot2.set_rmax(1.2*max)
mPlot2.set_title("CounterWeight 2 Throw Force(lbs)\nClockwise Rotation", va='bottom')
mPlot2.grid(True,which='major')
mPlot2.set_xticks(np.pi/180*np.linspace(0,360,24,endpoint=False))


# Calculate the position from acceleration
# import scipy.integrate
# def derivX(x, t, system):
#     return [x[1], system.accelerationX(t)]
#
# def derivY(y, t, system):
#     return [y[1], system.accelerationY(t)]
#
# state0=[0.0, 0.0]
# time = np.linspace(0, 3, num=1000)
# posX=scipy.integrate.odeint(derivX, state0, time, args=(system,))
# posY=scipy.integrate.odeint(derivY, state0, time, args=(system,))
# x=posX[:,0]
# y=posY[:,0]
#x=system.derivX(t)
#y=system.derivY(t)
# r=np.sqrt((x*x)+(y*y))
# theta=np.arctan2(x,y)
# max=np.max(r)

plt.show()