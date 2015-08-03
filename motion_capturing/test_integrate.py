__author__ = 'jr'
import numpy as np
import matplotlib.pyplot as plt

from motion_capturing.integrate import integrate


def main():
    fs = 1500.0  # Sampling Frequency (Hz)
    Ts = 1/fs  # Sample time, period
    f1 = 50.0  # Hz
    f2 = 120.0  # Hz

    # Compute the time vector
    t = np.arange(0.0, 1.2, Ts, dtype=float)
    omega1 = 2*np.pi*f1
    omega2 = 2*np.pi*f2

    x = 2.0*np.cos(omega1*t) + np.sin(omega2*t)
    v = -2.0*omega1*np.sin(omega1*t) + omega2*np.cos(omega2*t)
    a = -(omega1*omega1)*2*np.cos(omega1*t) - (omega2*omega2)*np.sin(omega2*t)
    calc_x, calc_v, freq, ffta = integrate(a, Ts)

    plt.subplot(4, 1, 1)
    plt.plot(t, a)
    plt.grid()
    plt.xlabel("time (t)")
    plt.ylabel("Accel (m/s/s)")
    plt.subplot(4, 1, 2)
    plt.plot(t, v)
    plt.plot(t, calc_v, '--r')
    plt.grid()
    plt.xlabel("time (t)")
    plt.ylabel("Vel (m/s)")
    plt.subplot(4, 1, 3)
    plt.plot(t, x)
    plt.plot(t, calc_x, '--r')
    plt.grid()
    plt.xlabel("time (t)")
    plt.ylabel("X (m)")
    plt.subplot(4, 1, 4)
    plt.plot(freq, np.abs(ffta), 'r')
    plt.grid()
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")

    plt.show()


# call main
if __name__ == '__main__':
    main()