import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import math
forward = 0
backward = 0

#salahli [0.5, 0.322, 1.15] [117.061, 117.036, 117.091]
#kur poylu [109.9,91] [-1.34,-1.6]
#realdata trednline [48.5,86.2,95.9] [-19.5,-18.8,-18.63]
#varvara sol =[155,131,128] [1.15,1.12,1.09]


def ln(forward,backward):
    # x and y data
    x = (np.asarray([48.5,86.2,95.9]))
    y = (np.asarray([-19.5,-18.8,-18.63]))
    # array of a and b coefficients in y = a*ln(x) + b
    coefficients = np.polyfit(np.log(x), y, 1)
    a = coefficients[0]
    b = coefficients[1]
    # Take forward and backward inputs from user and append to existing x array new values
    if forward != 0 and backward != 0:
       x = sorted(x)
       x = np.insert(x, 0, abs((x[0]-backward)))
       x = np.insert(x, len(x), (x[len(x)-1]+forward))
    elif forward == 0 and backward == 0:
       x = np.array(x)
    elif forward == 0:
        x = sorted(x)
        x = np.insert(x, 0, abs((x[0] - backward)))
    elif backward == 0:
        x = sorted(x)
        x = np.insert(x, len(x), (x[len(x) - 1] + forward))
    y = a * np.log(x) + b

    return x, y, a, b


# Plot the graph
def plot():
    x = ln(forward,backward)[0]
    y = ln(forward,backward)[1]
    plt.scatter(x, y,s=30)
    z = sorted(x.flatten())
    x_new = np.linspace(min(z), max(z), 15)
    a_BSpline = make_interp_spline(z, y,k=len(x)-1)
    y_new = a_BSpline(x_new)
    plt.grid(True)
    plt.title("Water consumption")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.plot(x, y)
    plt.show()
# Predcit x based on y
def predict(x):
    y = round(ln(forward,backward)[2] * np.log(x) + ln(forward,backward)[3], 2)
    return y

