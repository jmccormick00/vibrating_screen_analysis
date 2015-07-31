__author__ = 'jrmccormick'

import numpy as np
import matplotlib.pyplot as plt


def integrate(accel, T):
    # The integration method
    # Input:
    #       accel - the acceleration vector
    #       T - the period, the sampling time (t1 + T = t2)
    # Takes an array of acceleration values recorded at equally spaced time intervals
    # and performs a double integral on them to get displacement.
    # It performs the integration by converting the time(t) vs acceleration data from
    # time domain to frequency domain by utilizing a Fourier transform
    # In frequency domain a simplified form of displacement has the following form:
    # x = A*sin(omega*t)    Taking the derivative of x yields velocity and acceleration
    # v = omega*A*cos(omega*t)
    # a = -(omega*omega)*A*sin(omega*t)
    # Thus in frequency domain, to perform a double integral you divide acceleration by -(omega^2)
    # Once the division is performed, perform an inverse Fourier transform to get back time(t) vs displacement

    # First - Take the Fourier transform
    fft_a = np.fft.fft(accel)

    # Second - Calculate the frequencies based on the number of points and the period
    n = len(fft_a)
    half_n = np.ceil(n/2.0)
    freq = np.fft.fftfreq(n, T)

    # Third - Note that the frequencies in the FFT and the freq vector go from zero to some
    # large positive number then from a large negative number back toward zero. It is common
    # to look at just the first half of the unshifted FFT and frequency vectors and fold all the
    # amplitude info into the positive frequencies.  Furthermore, to get amplitude right, you must
    # normalize by the length of the original FFT.  Note the (2/n) in the following accomplishes
    # both the folding and scaling.
    amplitude_fold = (2.0 / n) * fft_a[:half_n]
    freq_fold = freq[:half_n]

    # Fourth - calculate omega and divide fft by -omega^2
    w = 2*np.pi*freq
    fft_x = fft_a / (-w*w)
    fft_x[0] = 0.0001  # make sure the first value isnt zero

    # Fifth - Convert the new fft_x vector back into time domain using an inverse
    # Fourier transform and return the displacement, frequencies, and amplitudes
    x = np.fft.ifft(fft_x)
    return x, freq_fold, amplitude_fold


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

    calc_x, freq, ffta = integrate(a, Ts)

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