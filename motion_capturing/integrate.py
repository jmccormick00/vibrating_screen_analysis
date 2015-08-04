__author__ = 'jrmccormick'

import numpy as np


def integrate(acceleration, T):
    """
    Takes an array of acceleration values recorded at equally spaced time intervals
    and performs a double integral on them to get displacement.
    It performs the integration by converting the time(t) vs acceleration data from
    time domain to frequency domain by utilizing a Fourier transform
    In frequency domain a simplified form of displacement looks like the following:
    x = A*sin(omega*t)    Taking the derivative of x yields velocity and acceleration
    v = omega*A*cos(omega*t)
    a = -(omega*omega)*A*sin(omega*t)
    Thus in frequency domain, to perform a double integral you divide acceleration by -(omega^2) and to get
    velocity you divide by (omega*j)
    Once the division is performed, perform an inverse Fourier transform to get back time(t) vs displacement
    :param acceleration: acceleration vector
    :param T: T - the period, the sampling time (t1 + T = t2)
    :return: the displacement vector, velocity, frequency vector, amplitude vector
    """

    # First - Take the Fourier transform
    fft_a = np.fft.fft(acceleration)

    # Second - Calculate the frequencies based on the number of points and the period
    n = len(fft_a)
    half_n = np.ceil(n/2.0)
    freq = np.fft.fftfreq(n, T)

    # Third - Note that the frequencies in the FFT and the freq vector go from zero to some
    # large positive number then from a large negative number back toward zero. It is common
    # to look at just the first half of the un-shifted FFT and frequency vectors and fold all the
    # amplitude info into the positive frequencies.  Furthermore, to get amplitude right, you must
    # normalize by the length of the original FFT.  Note the (2/n) in the following accomplishes
    # both the folding and scaling.
    amplitude_fold = (2.0 / n) * fft_a[:half_n]
    freq_fold = freq[:half_n]

    # Fourth - calculate omega
    w = 2*np.pi*freq
    if w[0] == 0:
        w[0] = 0.00001  # make sure the first value isn't zero
    # solve for displacement and velocity
    fft_v = fft_a / (w*complex(0.0, 1.0))
    fft_x = fft_a / (-w*w)
    fft_v[0] = complex(0.000001, 0.0000001)  # make sure the first value isn't zero
    fft_x[0] = complex(0.000001, 0.0000001)  # make sure the first value isn't zero

    # Fifth - Convert the new fft_x and fft_v vectors back into time domain using an inverse
    # Fourier transform and return the displacement, velocity, frequencies, and amplitudes
    x = np.fft.ifft(fft_x)
    v = np.fft.ifft(fft_v)
    return x.real, v.real, freq_fold, amplitude_fold
