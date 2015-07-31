__author__ = 'jrmccormick'

# Imports ======================================
import numpy as np
import scipy.integrate
from matplotlib import pyplot as plt
from matplotlib import gridspec

# Screen Constants ==================================
# Screen Eccentric mass
m0 = 683.2 #slugs
# Screen moment of inertia
J0 = 16297 #84153.8 #slugs*ft^2
# Screen body angle
alpha = -0.0 # radians
# Spring Feed stiffness
Sfx = 32736 #16368 #lb/ft
Sfy = 32736 #lb/ft
# Spring discharge stiffness
Sdx = 32736 #16368 #lb/ft
Sdy = 32736 #lb/ft
# Feed Spring placement
Xf = -8 #ft
Yf = 0.0 #ft
# Discharge Spring placement
Xd = 8.0 #ft
Yd = 0.0 #ft
# ===================================================
# Mechanism Constants ===============================
# Counterweight 1 & 3 mass
m1 = m3 = 8 #slugs
# Starting Angle
A1 = A3 = 4.7124 #Radians
# Counterweight 2 mass
m2 = 5 #slugs
# Lag Angle
LA = 1.0 # radians
A2 = A1 - LA
# Eccentric distance of mass
r = 0.5 # ft
# angular velocity
omega1 = omega3 = 200*(2*np.pi)/60 #rad/sec
omega2 = -omega1
# ===================================================

# Screen Adjusted Spring Stiffness
Sfax = Sfy*np.sin(alpha)+Sfx*np.cos(alpha)
Sfay = Sfy*np.cos(alpha)+Sfx*np.sin(alpha)
Sdax = Sdy*np.sin(alpha)+Sdx*np.cos(alpha)
Sday = Sdy*np.cos(alpha)+Sdx*np.sin(alpha)

fxArr = []
fyArr = []
fx1Arr = []
fx2Arr = []
fx3Arr = []
fy1Arr = []
fy2Arr = []
fy3Arr = []
DfxArr = []
DfyArr = []
DdxArr =[]
DdyArr=[]
TArr=[]

# Update Function ==============================
def screendynamics(state, t):
    X0 = state[0]
    dX0 = state[1]
    Y0 = state[2]
    dY0 = state[3]
    Theta0 = state[4]
    dTheta0 = state[5]


    fx1 = m1*r*omega1*omega1*np.cos(A1+omega1*t)
    fx2 = 0 #m2*r*omega2*omega2*np.cos(A2+omega2*t)
    fx3 = 0 #m3*r*omega3*omega3*np.cos(A3+omega3*t)

    fy1 = m1*r*omega1*omega1*np.sin(A1+omega1*t)
    fy2 = 0 #m2*r*omega2*omega2*np.sin(A2+omega2*t)
    fy3 = 0 #m3*r*omega3*omega3*np.sin(A3+omega3*t)

    fx1Arr.append(fx1)
    fx2Arr.append(fx2)
    fx3Arr.append(fx3)
    fy1Arr.append(fy1)
    fy2Arr.append(fy2)
    fy3Arr.append(fy3)
    fxArr.append(fx1 + fx2 + fx3)
    fyArr.append(fy1 + fy2 + fy3)

    # Screen Spring deformation
    Dfx = X0 + (Xf*np.cos(Theta0) - Yf*np.sin(Theta0)) - Xf
    Dfy = Y0 + (Xf*np.sin(Theta0) + Yf*np.cos(Theta0)) - Yf
    Ddx = X0 + (Xd*np.cos(Theta0) - Yd*np.sin(Theta0)) - Xd
    Ddy = Y0 + (Xd*np.sin(Theta0) + Yd*np.cos(Theta0)) - Yd

    TArr.append(t)
    DfxArr.append(Dfx)
    DfyArr.append(Dfy)
    DdxArr.append(Ddx)
    DdyArr.append(Ddy)

    # Screen Equations of motion
    ddX0 = ((fx1+fx2+fx3) - (2*Sfax*Dfx) - (2*Sdax*Ddx)) / m0
    ddY0 = ((fy1+fy2+fy3)-(2*Sfay*Dfy)-(2*Sday*Ddy)) / m0
    ddTheta0 = ((-Yd*2*Sdax*Ddx) + (Xd*2*Sday*Ddy) - (Yf*2*Sfax*Dfx) + (Xf*2*Sfay*Dfy)) / J0

    return [dX0, ddX0, dY0, ddY0, dTheta0, ddTheta0]

dt = .0001
end_t = 60
state0 = [0, 0, 0, 0, 0, 0]
time = np.linspace(0, end_t, num=end_t/dt)
dynamics = scipy.integrate.odeint(screendynamics, state0, time)
x0 = dynamics[:, 0]
y0 = dynamics[:, 2]
theta0 = dynamics[:, 4]

# Convert to inches
x0 = x0*12.0
y0 = y0*12.0
theta = np.arctan2(y0, x0)

# Convert the motion of x0 and y0 into polar coords
r=np.sqrt((x0*x0)+(y0*y0))
maxDisplacement=r.max()
rAngle=theta[np.argmax(r)]
if rAngle<0:
    rAngle=np.pi+rAngle

# set up the force arrays for plotting
fxVec=np.array(fxArr)
fyVec=np.array(fyArr)
rf=np.sqrt((fxVec*fxVec)+(fyVec*fyVec))
forceTheta=np.arctan2(fyVec, fxVec)

fx1Vec=np.array(fx1Arr)
fx2Vec=np.array(fx2Arr)
fx3Vec=np.array(fx3Arr)
fy1Vec=np.array(fy1Arr)
fy2Vec=np.array(fy2Arr)
fy3Vec=np.array(fy3Arr)

rf1=np.sqrt((fx1Vec*fx1Vec)+(fy1Vec*fy1Vec))
rf2=np.sqrt((fx2Vec*fx2Vec)+(fy2Vec*fy2Vec))
rf3=np.sqrt((fx3Vec*fx3Vec)+(fy3Vec*fy3Vec))

forceTheta1=np.arctan2(fy1Vec, fx1Vec)
forceTheta2=np.arctan2(fy2Vec, fx2Vec)
forceTheta3=np.arctan2(fy3Vec, fx3Vec)

max=np.argmax(rf)
resultAngle=forceTheta[max]
if resultAngle<0:
    resultAngle=np.pi+resultAngle

# set up the spring deformation arrays for plotting
deltaFY=np.array(DfyArr)*12
deltaFX=np.array(DfxArr)*12
deltaDX=np.array(DdxArr)*12
deltaDY=np.array(DdyArr)*12


fig=plt.figure(figsize=(20,20))
G=gridspec.GridSpec(4,4)
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
axes02.plot(time, theta0)

axes03=fig.add_subplot(G[0,3], polar=True, axisbg='#d5de9c')
axes03.set_title("CG Movement Profile\nThrow: {:.2f}(inch)@{:.2f}(deg)".format(maxDisplacement, np.rad2deg(rAngle)), va='bottom')
axes03.plot(theta[-4000:], r[-4000:])

axes10=fig.add_subplot(G[1,0], axisbg='#d5de9c')
axes10.set_xlabel('t(s)')
axes10.set_ylabel('delta(inch)')
axes10.set_xlim(TArr[0], TArr[-1])
axes10.set_title("Feed Spring Deformation X-axis", va='bottom')
axes10.plot(TArr, deltaFX)

axes11=fig.add_subplot(G[1,1], axisbg='#d5de9c')
axes11.set_xlabel('t(s)')
axes11.set_ylabel('delta(inch)')
axes11.set_xlim(TArr[0], TArr[-1])
axes11.set_title("Feed Spring Deformation Y-axis", va='bottom')
axes11.plot(TArr, deltaFY)

axes12=fig.add_subplot(G[1,2], axisbg='#d5de9c')
axes12.set_xlabel('t(s)')
axes12.set_ylabel('Force(lbs)')
axes12.set_xlim(TArr[0], TArr[-1])
axes12.set_title("Feed Spring Force X-axis", va='bottom')
axes12.plot(TArr, deltaFX*Sfax)

axes13=fig.add_subplot(G[1,3], axisbg='#d5de9c')
axes13.set_xlabel('t(s)')
axes13.set_ylabel('Force(lbs)')
axes13.set_xlim(TArr[0], TArr[-1])
axes13.set_title("Feed Spring Force Y-axis", va='bottom')
axes13.plot(TArr, deltaFY*Sfay)

axes20=fig.add_subplot(G[2,0], axisbg='#d5de9c')
axes20.set_xlabel('t(s)')
axes20.set_ylabel('delta(inch)')
axes20.set_xlim(TArr[0], TArr[-1])
axes20.set_title("Discharge Spring Deformation X-axis", va='bottom')
axes20.plot(TArr, deltaDX)

axes21=fig.add_subplot(G[2,1], axisbg='#d5de9c')
axes21.set_xlabel('t(s)')
axes21.set_ylabel('delta(inch)')
axes21.set_xlim(TArr[0], TArr[-1])
axes21.set_title("Discharge Spring Deformation Y-axis", va='bottom')
axes21.plot(TArr, deltaDY)

axes22=fig.add_subplot(G[2,2], axisbg='#d5de9c')
axes22.set_xlabel('t(s)')
axes22.set_ylabel('Force(lbs)')
axes22.set_xlim(TArr[0], TArr[-1])
axes22.set_title("Discharge Spring Force X-axis", va='bottom')
axes22.plot(TArr, deltaDX*Sdax)

axes23=fig.add_subplot(G[2,3], axisbg='#d5de9c')
axes23.set_xlabel('t(s)')
axes23.set_ylabel('Force(lbs)')
axes23.set_xlim(TArr[0], TArr[-1])
axes23.set_title("Discharge Spring Force Y-axis", va='bottom')
axes23.plot(TArr, deltaDY*Sday)


axes30=fig.add_subplot(G[3,0], polar=True, axisbg='#d5de9c')
axes30.set_title("Mechanism #1 Throw Force(lbs) Profile", va='bottom')
axes30.plot(forceTheta1, rf1)

axes31=fig.add_subplot(G[3,1], polar=True, axisbg='#d5de9c')
axes31.set_title("Mechanism #2 Throw Force(lbs) Profile", va='bottom')
axes31.plot(forceTheta2, rf2)

axes32=fig.add_subplot(G[3,2], polar=True, axisbg='#d5de9c')
axes32.set_title("Mechanism #3 Throw Force(lbs) Profile", va='bottom')
axes32.plot(forceTheta3, rf3)

axes33=fig.add_subplot(G[3,3], polar=True, axisbg='#d5de9c')
axes33.set_title("Mechanism Combined Throw Force(lbs) Profile\nEllipse Angle:{:.2f}(deg)".format(np.rad2deg(resultAngle)), va='bottom')
axes33.plot(forceTheta, rf)

plt.tight_layout()
plt.show()