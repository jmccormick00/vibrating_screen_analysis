__author__ = 'jrmccormick'

import screen
import numpy as np
from integrate import integrate
import matplotlib.pyplot as plt

def main():
    fs = 500.0  # Sampling Frequency (Hz)
    Ts = 1/fs  # Sample time, period

    # Compute the time vector
    t = np.arange(0.0, 3.0, Ts, dtype=float)

    scr = screen.Screen(weight=111000.00, momentInertia=0.0)
    cw1 = screen.CounterWeight(posX=0.0,posY=0.0, radius=0.5, weight=300.0, rpm=800.0, startAngle=270.0, counterclockwise=False)
    cw2 = screen.CounterWeight(posX=0.0,posY=0.0, radius=0.5, weight=300.0, rpm=800.0, startAngle=270.0, counterclockwise=False)
    scr.addCounterWeight(cw1)
    scr.addCounterWeight(cw2)

    ax, ay = scr.calculate_acceleration(t)
    x, _, freq_x, ffta_x = integrate(ax, Ts)
    y, _, freq_y, ffta_y = integrate(ay, Ts)

    # Convert the motion of x and y into polar coords
    r = np.sqrt((x*x)+(y*y))
    theta = np.arctan2(y, x)

    plt.subplot(311)
    plt.plot(t, ax)
    plt.grid()
    plt.xlabel("time (t)")
    plt.ylabel("Accel (ft/s/s)")
    plt.subplot(312, polar=True)
    plt.plot(theta, r, '--r')
    plt.title("CG Movement Profile")
    plt.subplot(313)
    plt.plot(freq_x, np.abs(ffta_x), 'r')
    plt.grid()
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.show()


# call main
if __name__ == '__main__':
    main()