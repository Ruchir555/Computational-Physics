from matplotlib import pyplot
import numpy as np
from scipy import signal
import csv
import math
import pandas


dt = 0.001
t1 = np.arange(0.0, 10.0, dt)
r = np.exp(-t1[:1000]/0.05)               # impulse response
x = np.random.randn(len(t1))
s = 10*np.convolve(x, r)[:len(x)]*dt  # colored noise


t = np.arange(0., 10., 0.02)
x0 = 1
damp_rate = 1
omega = 5

x = np.arange(0., 10., 0.2)
def x(t):
    if(t.any() > 0):
        return (x0)*np.exp(-.5*(damp_rate)*t)*np.sin(omega*t)
    else:
        return 0

def envelope(t):
    return np.exp(-(damp_rate)*t/2)

def return_zero(t):
    return 0*t

def dirac_delta(t):
    if(t.any==0):
        return 1
    else:
        return 0

def deltagauss(x,b,sigma):
    arg=(-x**2/(2*sigma**2))
    num=np.exp(arg)
    den=sigma*np.sqrt(2*np.pi)
    delta=num/den
    return delta

# Main Plot of oscillator
pyplot.plot (t1,x(t1) + s, 'b-', t, envelope(t), 'g--', t, -envelope(t), 'g--')
pyplot.ylabel('x(t) [A.U.]')
pyplot.xlabel('t [s]')
pyplot.title('Damped Mechanical Oscillator with Gaussian Noise')
pyplot.annotate(r'$e^{\frac{-\Gamma_{m}}{2}t}$', xy = (2, 1), xytext=(2, 0.5), color='g').set_fontsize(20)
pyplot.annotate(r'$x(t) = x_{0} e^{\frac{-\Gamma_{m}}{2}t} sin(\Omega_{m}t)$', xy = (4, -0.75), xytext=(4, -1.00)).set_fontsize(20)
pyplot.annotate(r'$\Gamma_{m} = 1$', xy = (1, 1), xytext=(4, 0.85)).set_fontsize(12)
pyplot.annotate(r'$\Omega_{m} = 5$', xy = (1, 1), xytext=(4, 0.65)).set_fontsize(12)



# Embedded axis plot of impulse force
a = pyplot.axes([.725, .67, .2, .2])
# pyplot.plot(return_zero(t), 'r--')
pyplot.title('Impulse Force')
pyplot.ylabel('F(t) [A.U.]')
pyplot.xlabel('t [s]')
pyplot.xlim(-1, 1)
pyplot.ylim(-3,40)
#pyplot.xticks([])
pyplot.yticks([0],[])
# pyplot.axhline(y=0, color='k')
# pyplot.axvline(x=0, color='k')
impulse_x = np.linspace(-1,1,200)
impulse_y = deltagauss(impulse_x, 0, 0.01)
a.plot(impulse_x, impulse_y, 'r')


pyplot.show()





# Failed code == code junkyard
# ax = pyplot.axes()
# ax.arrow(0.1, 0, 0, 0.7, head_width=0.05, head_length=0.1, fc='k', ec='k')
# pyplot.show()
# a.annotate("", xy=(9, 0.75), xytext=(7.5, 0.5), arrowprops=dict(arrowstyle="->"))
# a.arrow(8, 0.5, 0, 0.2, length_includes_head=True, head_width = 0.5, head_length= 0.08)
# imp = signal.unit_impulse(2)
# a.plot(np.arange(-1, 1), imp)
# pyplot.annotate("",
#             xy=(0, 0), xycoords='data',
#             xytext=(1, 1), textcoords='data',
#             arrowprops=dict(arrowstyle="->",
#                             connectionstyle="arc3"),
#             )
# pyplot.arrow(7.9, 0, 0, 0.9, head_width=0.3, head_length=0.1, fc='k', ec='k')