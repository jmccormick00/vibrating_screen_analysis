__author__ = 'jrmccormick'

import screen
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import gridspec

cw1=screen.counterweight(posX=1.5,posY=-2, radius=0.5, weight=160, rpm=800, startAngle=270, counterclockwise=True)
cw2=screen.counterweight(posX=-2.95,posY=2.21, radius=0.5, weight=160, rpm=800, startAngle=270-90, counterclockwise=False)

cwArr=[cw1,cw2]
dt=.01
end_t=60
time = np.linspace(0, end_t, num=end_t/dt)
Xarr=[]
Yarr=[]
for t in time:
    x=0
    y=0
    for cw in cwArr:
        cw.calculateForces(t)
        x+=cw.fx
        y+=cw.fy
    Xarr.append(x)
    Yarr.append(y)