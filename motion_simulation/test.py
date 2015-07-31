__author__ = 'jrmccormick'

import screen
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import gridspec

#cw1=screen.counterweight(posX=0,posY=0, radius=0.5, weight=160, rpm=200, startAngle=270, counterclockwise=True)
cw2=screen.counterweight(posX=0,posY=0, radius=0.5, weight=160, rpm=800, startAngle=270-90, counterclockwise=False)
cw3=screen.counterweight(posX=0,posY=0, radius=0.5, weight=320, rpm=800, startAngle=270, counterclockwise=True)

cwArr=[cw2,cw3]
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

Xarr=np.array(Xarr)
Yarr=np.array(Yarr)
r=np.sqrt((Xarr*Xarr)+(Yarr*Yarr))
theta=np.arctan2(Xarr, Yarr)

fig=plt.figure(figsize=(6,6))
G=gridspec.GridSpec(1,1)
axes03=fig.add_subplot(G[0,0], polar=True, axisbg='#d5de9c')
#axes03.set_title("CG Movement Profile\nThrow: {:.2f}(inch)@{:.2f}(deg)".format(maxDisplacement, np.rad2deg(rAngle)), va='bottom')
axes03.plot(theta[-2000:], r[-2000:])

plt.show()