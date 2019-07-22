from pylab import *
from scipy.optimize import leastsq
from numpy import random


def residuals(p, y, t):
    err = y - sine_signal(t, p)
    return err


def sine_signal(t, p):
    return p[0] * sin(2 * pi * t / p[1] + p[2])


# number of points in original time series
n = 80

# time dimension: we generate the time values
t = linspace(0, 20, n)
signal_amp = 3.0
phase = -pi / 6
period = 6.0

p = signal_amp, period, phase
signal = sine_signal(t, p)

# introduce noise into the signal
noise_amp = 0.2 * signal_amp
noise = noise_amp * random.standard_normal(n)
signal_plus_noise = signal + noise
# initial guess of parameters
p0 = 10 * signal_amp, 1.3 * period, 1.8 * phase

# perform least square fit
plsq = leastsq(residuals, p0, args=(signal_plus_noise, t))

# plot data and fit curve
plot(t, signal, 'bo')
plot(t, signal_plus_noise, 'ko')
plot(t, sine_signal(t, plsq[0]), 'r--')
legend(('Signal', 'Signal+noise', 'fit'), loc='best')
title('Fit for a time series')
show()

from pylab import *
from scipy.optimize import leastsq
from numpy import random


def residuals(p, v, t):
    err = v - velocity(t, p)
    return err


def velocity(t, p):
    return p * t


# number of points in original time series
n = 100

# time dimension: we generate the time values
t = linspace(0, 20, n)

# initial guess for acceleration
p0 = 5
# actual signal
signal = velocity(t, 9.81)

# introduce noise into the signal
noise = 0.1 * signal * random.standard_normal(n)
signal_plus_noise = signal + noise

# perform least square fit
plsq = leastsq(residuals, p0, args=(signal_plus_noise, t))

# plot data and fit curve
plot(t, signal, 'bo')
plot(t, signal_plus_noise, 'ko')
plot(t, velocity(t, plsq[0]), 'ro-')
legend(('Signal', 'Signal+noise', 'fit'), loc='best')
title('Fit for a time series')
show()