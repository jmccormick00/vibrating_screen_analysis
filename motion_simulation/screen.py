__author__ = 'jrmccormick'

import numpy as np

class counterweight:
    def __init__(self, posX, posY, radius, weight, rpm, startAngle, counterclockwise):
        '''
        :param posX: The x position in relation to the center of gravity (ft)
        :param posY: The y position in relation to the center of gravity (ft)
        :param radius: the distance from the center of rotation to the center of gravity. (ft)
        :param weight: the weight of the counter weight. (lbs)
        :param rpm: rotations per min
        :param startAngle: The angle in which the center of gravity starts at (degrees)
        :param counterclockwise: the direction of rotation (True/False)
        '''
        self.posX=posX
        self.posY=posY
        self.rpm=rpm #rotations/min
        self.omega=rpm*(2*np.pi)/60 # rad/sec
        self.radius=radius # ft
        self.weight=weight # lbs
        self.mass=weight/32.17405 # slugs
        self.startAngle=np.deg2rad(startAngle)
        self.fr=self.fx=self.fy=self.theta=None
        if not counterclockwise:
            self.omega=-self.omega


    def calculateForces(self, t):
        '''
        :param t: A single time or an array of the time instances to use to solve the forces
        Stores the x and y values of the forces in fx and fy and calculates the resultant forces, fr
        '''
        self.fx=self.forceX(t)
        self.fy=self.forceY(t)
        self.fr=np.sqrt((self.fx*self.fx)+(self.fy*self.fy))
        self.theta=np.arctan2(self.fy, self.fx)

    def forceX(self, t):
        return self.mass*self.omega*self.omega*self.radius*np.cos(self.startAngle+self.omega*t)

    def forceY(self, t):
        return self.mass*self.omega*self.omega*self.radius*np.sin(self.startAngle+self.omega*t)-self.weight


class screen:
    def __init__(self, weight, momentInertia, alpha, feedSpringPos, dischargeSpringPos, feedSpringStiff, dischargeSpringStiff):
        # Adjusted Spring Stiffness based on screen body angle
        self.Sfax=feedSpringStiff[1]*np.sin(alpha)+feedSpringStiff[0]*np.cos(alpha)
        self.Sfay=feedSpringStiff[1]*np.cos(alpha)+feedSpringStiff[0]*np.sin(alpha)
        self.Sdax=dischargeSpringStiff[1]*np.sin(alpha)+dischargeSpringStiff[0]*np.cos(alpha)
        self.Sday=dischargeSpringStiff[1]*np.cos(alpha)+dischargeSpringStiff[0]*np.sin(alpha)

        self.mass=weight/32.17405 # slugs
        self.weight=weight
        self.alpha=np.deg2rad(alpha) # Body angle, radians
        self.momentInertia=momentInertia
        self.feedSpringPos=feedSpringPos
        self.dischargeSpringPos=dischargeSpringPos
        self.feedSpringStiff=feedSpringStiff
        self.dischargeSpringStiff=dischargeSpringStiff

        self.cwArr=[]

    def addCounterWeight(self, cw):
        self.cwArr.append(cw)

    def update(self, state, t):
        X0 = state[0]
        dX0 = state[1]
        Y0 = state[2]
        dY0 = state[3]
        #Theta0 = state[4]
        #dTheta0 = state[5]

        Theta0=0.0
        rx=ry=0.0
        mrx=mry=0.0
        for cw in self.cwArr:
            cw.calculateForces(t)
            rx += cw.fx
            ry += cw.fy
            mrx += cw.fx*cw.posY
            mry += cw.fy*cw.posX

        Dfx=X0+(self.feedSpringPos[0]*np.cos(Theta0)-self.feedSpringPos[1]*np.sin(Theta0))-self.feedSpringPos[0]
        Dfy=Y0+(self.feedSpringPos[0]*np.sin(Theta0)+self.feedSpringPos[1]*np.cos(Theta0))-self.feedSpringPos[1]
        Ddx=X0+(self.dischargeSpringPos[0]*np.cos(Theta0)-self.dischargeSpringPos[1]*np.sin(Theta0))-self.dischargeSpringPos[0]
        Ddy=Y0+(self.dischargeSpringPos[0]*np.sin(Theta0)+self.dischargeSpringPos[1]*np.cos(Theta0))-self.dischargeSpringPos[1]

        ddX0=(rx-(2*self.Sfax*Dfx)-(2*self.Sdax*Ddx))/self.mass
        ddY0=(ry-(2*self.Sfay*Dfy)-(2*self.Sday*Ddy))/self.mass
        #ddTheta0=(mry+mrx+(-self.dischargeSpringPos[1]*2*self.Sdax*Ddx)+(self.dischargeSpringPos[0]*2*self.Sday*Ddy)-(self.feedSpringPos[1]*2*self.Sfax*Dfx)+(self.feedSpringPos[0]*2*self.Sfay*Dfy))/self.momentInertia

        return [dX0, ddX0, dY0, ddY0] #, dTheta0, ddTheta0]