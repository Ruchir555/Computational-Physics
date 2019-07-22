from matplotlib import pyplot
import numpy as np
import csv
import math
import pandas


t = np.arange(0., 10., 0.02)
x0 = 1
damp_rate = 1
omega = 50

x = np.arange(0., 10., 0.2)
def x(t):
    return (x0)*np.exp(-.5*(damp_rate)*t)*np.sin(omega*t)

pyplot.plot (t,x(t), 'bo')
pyplot.ylabel('x(t)')
pyplot.xlabel('t')
pyplot.title('Mechanical Oscillator')
pyplot.show()


print("Hi")
i = 15
while(i>10):
    i-=1
    print(i)

# random plot
x = [1, 2, 3, 4, 5, 6, 7]
y = [1, 2, 3, 4, 5, 6, 7]
pyplot.plot(x,y)
pyplot.ylabel('some numbers')
pyplot.title('A graph')
pyplot.show()

# evenly sampled time at 200ms intervals
t = np.arange(0., 5., 0.2)

# red dashes, blue squares and green triangles
pyplot.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
pyplot.show()


# histogram
mu, sigma = 100, 15
x = mu + sigma * np.random.randn(10000) #generates Gaussian data

# the histogram of the data
n, bins, patches = pyplot.hist(x, 50, density=1, facecolor='g', alpha=0.75)


pyplot.xlabel('Smarts')
pyplot.ylabel('Probability')
pyplot.title('Histogram of IQ')
pyplot.text(60, .025, r'$\mu=100,\ \sigma=15$')
pyplot.axis([40, 160, 0, 0.03])
pyplot.grid(True)
pyplot.show()

# This is to get the current working directory
import os
cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in '%s': %s" % (cwd, files))






# CSV stuff

# Another way to tell the open() function where your file is located is by using an absolute path, e.g.:
# f = open("/Users/foo/address.csv")

with open("random_data.csv") as file:
    reader = csv.reader(file)

    count = 0

    # the histogram of the data from the csv file
    # for rows in reader:
    #     pyplot.hist(rows[0], 50, density=1, facecolor='g', alpha=0.75)

    sigma_accum = 0
    mu_accum = 0
    for rows in reader:
        if (rows[0] != 'normal'):
            # print(rows[0])        #prints numbers
            #print(type(rows[0]))   #<class 'str'>
            mu_accum += float(rows[0])
    print("mu_accum", mu_accum)
    mu = mu_accum/100
    print("mu:", mu)

    print("count", count)
    count = 0
    rows = 0

    sigma_accum = 0
    for rows in reader:
        if (rows[0] != 'normal'):
            sigma_accum += (float(rows[0]) - mu)**2
            print("test:", sigma_accum)

    print("sigma_accum:", sigma_accum)
    sigma = math.sqrt((sigma_accum/100))
    print("sigma:", sigma)

#todo
    # why is sigma_accum giving 0?? sketchy...
    # because of initialization
    # for some reason not iterating through reader second time...


    # mu, sigma = 0, .1
    for rows in reader:
        if(rows[0] != 'normal'):
            x = mu + sigma * float(np.array(rows[0]))

    pyplot.hist(x, 100, density=1, facecolor='b', alpha=0.75)

    pyplot.xlabel('Data')
    pyplot.ylabel('Probability')
    pyplot.title('Histogram of Random Data')
    pyplot.text(-.75, .25, r'$\mu=-0.005,\ \sigma=0$')
    pyplot.axis([-1, 1, 0, 0.3])
    pyplot.grid(True)
    pyplot.show()


