__author__ = 'jrmccormick'

import numpy as np
import matplotlib.pyplot as plt

from motion_capturing.integrate import integrate


def read_datafile(filename):
    X = []
    Y = []
    Z = []

    datafile = open(filename)
    for line in datafile:
        x, y, z = line.split()
        X.append(float(x))
        Y.append(float(y))
        Z.append(float(z))
    datafile.close()

    return np.array(X), np.array(Y), np.array(Z)


def main():
    fs = 1500.0  # Sampling Frequency (Hz)
    Ts = 1/fs  # Sample time, period

    # Compute the time vector
    t = np.arange(0.0, 0.2, Ts, dtype=float)

    calc_x, calc_v, freq, ffta = integrate(a, Ts)

    plt.subplot(3,1,1)
    plt.plot(t, a)
    plt.grid()
    plt.xlabel("time (t)")
    plt.ylabel("Accel (m/s/s)")
    plt.subplot(3,1,2)
    plt.plot(t, calc_x, '--r')
    plt.legend()
    plt.grid()
    plt.xlabel("time (t)")
    plt.ylabel("X (m)")
    plt.subplot(3,1,3)
    plt.plot(freq, np.abs(ffta), 'r')
    plt.grid()
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")

    plt.show()


# call main
if __name__ == '__main__':
    main()