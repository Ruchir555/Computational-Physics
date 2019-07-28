from scipy.integrate import *
import math
import numpy as np
from pylab import *
import matplotlib.pyplot as plt

# Function to integrate
function_map = lambda x: math.exp(-x**2)

def function(x):
    return math.exp(-x**2)

def integrate(function, time, dt):
    for t in np.nditer(time):
        accum = dt * function
    return accum

# Integration bounds
lower_bound = -5
upper_bound = 5
number_of_points = 500

# Differential time element
t = np.linspace(lower_bound, upper_bound, num = number_of_points)
dt = t[1] - t[0]
# print("dt:", dt)

# Scipy integration method
scipy_result = quad(function_map, lower_bound, upper_bound)
print("Scipy Result\n Value, Error:", scipy_result)

# My integration method
f1 = np.vectorize(function)
my_result = integrate(f1(t), t, dt)
integrated_value = 0
for element in my_result:
    integrated_value += element

# print(my_result)
print("\nMy result:", integrated_value)

error = abs(scipy_result[0] - integrated_value)
print("\nScipy result - my result:", error)

# print((pi)**0.5)      # Exact value

# Plotting function
plt.plot(t, f1(t), 'r--')
plt.fill_between(t, f1(t), facecolor = 'blue', alpha = 1)
xlabel('$x$')
ylabel('$f(x)$')
plt.grid()
title('$e^{-x^2}$')
plt.show()

error_ydata = []
index = []
convergence_n = 52
# Convergence plot error data generation
for n in range(2,convergence_n):
    index += [n]
    integrated_value2 = 0
    integral_value = 0
    number_of_points = n
    t2 = np.linspace(lower_bound, upper_bound, num=number_of_points)
    dt2 = t2[1] - t2[0]
    f2 = np.vectorize(function)
    my_result2 = integrate(f2(t2), t2, dt2)
    for elements in my_result2:
        integrated_value2 += elements
        integral_value += elements
    error_ydata += [integrated_value2]

# Compute best value error:
best_error = abs(error_ydata[-1] - (pi**0.5))
print("\nBest error from my method:", best_error, 'N,', convergence_n)
print("Best value:", integrated_value, 'N:', convergence_n )


# Convergence plot
plt.plot(index, error_ydata, 'b--')
plt.axhline(y=pi**0.5, color='r', linestyle='-')
plt.title("Convergence plot of methods")
xlabel('$N$ (Number of time partitions)')
ylabel('$\int f(x) dx$')
legend(('My method convergence values', 'Exact solution, $\pi^{1/2}$'), loc='best')
plt.show()
