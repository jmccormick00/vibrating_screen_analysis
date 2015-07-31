__author__ = 'jrmccormick'

import numpy as np

class CounterWeight:
    def __init__(self, radius, weight, rpm, startAngle, counterclockwise):
        '''
        :param radius: the distance from the center of rotation to the center of gravity. (ft)
        :param weight: the weight of the counter weight. (lbs)
        :param rpm: rotations per min
        :param startAngle: The angle in which the center of gravity starts at (degrees)
        :param counterclockwise: the direction of rotation (True/False)
        '''
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
        self.fx=self.forceX(t)
        self.fy=self.forceY(t)
        self.fr=np.sqrt((self.fx*self.fx)+(self.fy*self.fy))
        self.theta=np.arctan2(self.fy, self.fx)

    def forceX(self, t):
        return self.mass*self.omega*self.omega*self.radius*np.cos(self.startAngle+self.omega*t)

    def forceY(self, t):
        return self.mass*self.omega*self.omega*self.radius*np.sin(self.startAngle+self.omega*t)-self.weight

class MechanismSystem:
    def __init__(self, weight, centerWeight, rpm, radius, lagAngle):
        self.m1=CounterWeight(radius=radius, weight=weight, rpm=rpm, startAngle=270, counterclockwise=True)
        self.m2=CounterWeight(radius=radius, weight=centerWeight, rpm=rpm, startAngle=270-lagAngle, counterclockwise=False)
        self.m3=CounterWeight(radius=radius, weight=weight, rpm=rpm, startAngle=270, counterclockwise=True)
        self.fr=self.frx=self.fry=self.theta=self.resultAngle=None

    def calculateForces(self, t):
        self.m1.calculateForces(t)
        self.m2.calculateForces(t)
        self.m3.calculateForces(t)
        # Solve the resultant force
        self.frx = self.m1.fx + self.m2.fx + self.m3.fx
        self.fry = self.m1.fy + self.m2.fy + self.m3.fy
        self.fr=np.sqrt((self.frx*self.frx)+(self.fry*self.fry))
        self.theta=np.arctan2(self.fry, self.frx)
        max=np.argmax(self.fr)
        self.resultAngle=self.theta[max]
        if self.resultAngle<0:
            self.resultAngle=np.pi+self.resultAngle