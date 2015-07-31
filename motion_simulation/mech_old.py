__author__ = 'jrmccormick'

import numpy as np
from math import sqrt
from matplotlib import pyplot as plt
from matplotlib import animation

#==============CONSTANTS========================
# Gravity
g = 32.17405 # ft/s^2

#==========MECHANISM PARAMETERS=================
# Mass
m = 6.5 # slugs
omega = 30 # rad/s 83.7
# Radius to center of mass
radius_ctr_mass = 1.0 # ft

# Center of gravity starting angle
theta0 = np.pi/4 # radians

thetaArr = []
pXArr = []
pYArr = []
pRArr = []

#==========ANIMATION PARAMETERS=================
frames = 360

#============================================
# Set up figures for plotting
fig = plt.figure()
thetaPlot = fig.add_subplot(411, xlim=(-3, 3), ylim=(-3, 3))
thetaPlot.grid(True)
title = thetaPlot.set_title("")

Xaxis = fig.add_subplot(412, xlim=(0,7), ylim=(-600,600))
Xaxis.grid(True)
Xaxis.set_title("Fx (lb)")
Fx_line, = Xaxis.plot([],[], c='r')

Yaxis = fig.add_subplot(413, xlim=(0,7), ylim=(-900,900))
Yaxis.grid(True)
Yaxis.set_title("Fy (lb)")
Fy_line, = Yaxis.plot([],[], c='b')

Raxis = fig.add_subplot(414, xlim=(0,7), ylim=(-900,900))
Raxis.grid(True)
Raxis.set_title("Fr (lb)")
Fr_line, = Raxis.plot([],[], c='g')


# Calculate the center position
cX = radius_ctr_mass * np.cos(theta0)
cY = radius_ctr_mass * np.sin(theta0)
ctr_mass = plt.Circle((cX, cY), radius=0.1, fc='r')

def init():
    Fx_line.set_data([],[])
    Fy_line.set_data([],[])
    Fr_line.set_data([],[])
    ctr_mass.center = (cX, cY)
    thetaPlot.add_patch(ctr_mass)
    title.set_text("")
    return (ctr_mass, title, Fx_line, Fy_line)

def animate(i):
    #============================================
    # Update the position of the center of mass
    x, y = ctr_mass.center
    x = radius_ctr_mass * np.sin(theta0 + np.radians(-i))
    y = radius_ctr_mass * np.cos(theta0 + np.radians(-i))
    ctr_mass.center = (x, y)
    title.set_text("Theta: {:.2f} | radians/s: {:.2f} | rpm: {:.2f}".format(np.radians(i), omega, omega/(2*np.pi)*60))
    #=============================================

    thetaArr.append(np.radians(i))
    #============================================
    # Update the x forces
    px = m*(omega*radius_ctr_mass*radius_ctr_mass*np.cos(np.radians(-i)))
    pXArr.append(px)
    Fx_line.set_data(thetaArr,pXArr)
    #============================================

    # Update the y forces
    py = m*g + m*(omega*radius_ctr_mass*radius_ctr_mass*np.sin(np.radians(-i)))
    pYArr.append(py)
    Fy_line.set_data(thetaArr,pYArr)
    #============================================

    #============================================
    # Calculate the resultant force magnitude
    pr = sqrt((px*px) + (py*py))
    pRArr.append(pr)
    Fr_line.set_data(thetaArr,pRArr)

    return (ctr_mass, title, Fy_line, Fx_line, Fr_line)

anim=animation.FuncAnimation(fig, animate, init_func=init, frames=frames, interval=30, blit=False, repeat=False)
plt.show()

