__author__ = 'jrmccormick'

# Imports ======================================
import screen_old
import numpy as np
import scipy.integrate
from matplotlib import pyplot as plt
from matplotlib import gridspec


# Screen Constants ==================================
# Screen moment of inertia
J0 = 16297 #84153.8 #slugs*ft^2
# ===================================================
sc = screen_old.screen(weight=22100, momentInertia=J0, alpha=0.0, feedSpringPos=(-8.0, 0.0), dischargeSpringPos=(8.0, 0.0),
                   feedSpringStiff=(32763, 32763), dischargeSpringStiff=(32736, 32736))
cw1 = screen_old.counterweight(posX=0, posY=0, radius=0.5, weight=257.8, rpm=200, startAngle=270, counterclockwise=False)
#cw2=screen.counterweight(posX=0,posY=0, radius=0.5, weight=160, rpm=200, startAngle=270-90, counterclockwise=False)
#cw3=screen.counterweight(posX=0,posY=0, radius=0.5, weight=160, rpm=200, startAngle=270, counterclockwise=True)

sc.addCounterWeight(cw1)
#sc.addCounterWeight(cw2)
#sc.addCounterWeight(cw3)

# Update Function ==============================
def screendynamics(state, t, sc):
    return sc.update(state, t)

dt=.0001
end_t=60
state0=[0,0,0,0,0,0]
time = np.linspace(0, end_t, num=end_t/dt)
dynamics=scipy.integrate.odeint(screendynamics, state0, time, args=(sc,))
x0=dynamics[:,0]
y0=dynamics[:,2]
#theta0=dynamics[:,4]

# Convert to inches
x0=x0*12.0
y0=y0*12.0
theta=np.arctan2(y0, x0)

# Convert the motion of x0 and y0 into polar coords
r=np.sqrt((x0*x0)+(y0*y0))
maxDisplacement=r.max()
rAngle=theta[np.argmax(r)]
if rAngle<0:
    rAngle=np.pi+rAngle

fig=plt.figure(figsize=(20,20))
G=gridspec.GridSpec(1,4)
axes00=fig.add_subplot(G[0,0], axisbg='#d5de9c')
axes00.set_xlabel('t(s)')
axes00.set_ylabel('X0(inch)')
axes00.set_title("Screen Body Movement X-axis", va='bottom')
axes00.plot(time, x0)

axes01=fig.add_subplot(G[0,1], axisbg='#d5de9c')
axes01.set_xlabel('t(s)')
axes01.set_ylabel('Y0(inch)')
axes01.set_title("Screen Body Movement Y-axis", va='bottom')
axes01.plot(time, y0)

axes02=fig.add_subplot(G[0,2], axisbg='#d5de9c')
axes02.set_xlabel('t(s)')
axes02.set_ylabel('Theta0(radians)')
axes02.set_title("Screen Body Angular Displacement", va='bottom')
#axes02.plot(time, theta0)

axes03=fig.add_subplot(G[0,3], polar=True, axisbg='#d5de9c')
axes03.set_title("CG Movement Profile\nThrow: {:.2f}(inch)@{:.2f}(deg)".format(maxDisplacement, np.rad2deg(rAngle)), va='bottom')
axes03.plot(theta[-4000:], r[-4000:])

plt.tight_layout()
plt.show()