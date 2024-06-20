import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# optimization function for 1 variable
def optimize1d(f1, f2, xmin, xmax, initialguess):
    xbase = np.linspace(xmin, xmax, 250)
    ybase = f1(xbase)

    # initializing guess
    bestx = initialguess

    # plotting out the function
    global fig, ax
    ax.plot(xbase, ybase)
    xall, yall = [], []
    lnall,  = ax.plot([], [], 'ro-')
    lngood, = ax.plot([], [], 'go', markersize=10)

    # Learning rate 
    lr = 0.1

    # number of iterations
    num_epochs = 100

    # definiting a function to plot per iteration
    def onestepderiv(frame):
        nonlocal bestx, lr
        xall.append(bestx)
        yall.append(f1(bestx))

        # update step
        x = bestx - f2(bestx) * lr 
        bestx = x
        y = f1(x)

        # appending to lists
        lngood.set_data([x], [y])
        lnall.set_data(xall, yall)

        # printing final output
        if (frame == num_epochs - 1):
            print(x, y)

    # animating the process
    ani = FuncAnimation(fig, onestepderiv, frames=range(num_epochs), interval=100, repeat=False)
    return ani

def optimize2d(f, df_x, df_y, xmin, xmax, ymin, ymax, initialguess_x, initialguess_y):
    xbase = np.linspace(xmin, xmax, 50)
    ybase = np.linspace(ymin, ymax, 50)
    zbase = f(xbase, ybase)

    #update step
    bestx = initialguess_x
    besty = initialguess_y 

    global fig, ax
    X, Y = np.meshgrid (xbase, ybase)
    Z = f(X, Y)

    # plotting the function
    ax.plot_surface(X, Y, Z, alpha = 0.5)
    xall, yall, zall = [], [], []
    lnall,  = ax.plot([], [], [], 'ro-')
    lngood, = ax.plot([], [], [], 'go', markersize = 10)

    # Learning rates
    lr_x = 0.1
    lr_y = 0.1

    # number of iterations
    num_epochs = 100

    def onestepderiv(frame):
        nonlocal bestx, besty, lr_x, lr_y
        xall.append(bestx)
        yall.append(besty)
        zall.append(f(bestx, besty))

        # update step
        x = bestx - df_x(bestx, besty) * lr_x
        y = besty - df_y(bestx, besty) * lr_y 
        bestx = x
        besty = y
        z = f(x, y)

        # appending to the lists
        lngood.set_data([x], [y])
        lngood.set_3d_properties(z)
        lnall.set_data(xall, yall)
        lnall.set_3d_properties(zall)

        # printing final output
        if (frame == num_epochs - 1):
            print(x, y, f(x, y))

    # animating the process
    ani = FuncAnimation(fig, onestepderiv, frames=range(num_epochs), interval=10, repeat=False)
    return ani

# function f1
def f1(x):
    return x ** 2 + 3 * x + 8
def df1(x):
    return 2 * x + 3

# function f5
def f5(x):
    return (np.cos(x))**4 - (np.sin(x))**3 - 4*(np.sin(x)**2) + np.cos(x) + 1
def df5(x):
    return (- np.cos(x)**3 * np.sin(x)) - (3 * np.sin(x)**2 * np.cos(x)) - (8 * np.sin(x) * np.cos(x)) - np.sin(x)

# uncomment the below for 1D optimization
# fig, ax = plt.subplots()
# ani = optimize1d(f1, df1, -5, 5, 4)
# ani = optimize1d(f5, df5, 0, 2 * np.pi, 3)

# function f3
def f3(x, y):
    return x**4 - 16*x**3 + 96*x**2 - 256*x + y**2 - 4*y + 262

def df3_dx(x, y):
    return 4*x**3 - 48*x**2 + 192*x - 256

def df3_dy(x, y):
    return 2*y - 4

# function f4
def f4(x, y):
    return np.exp(-(x - y)**2) * np.sin(y)

def df4_dx(x, y):
    return -2 * np.exp(-(x - y)**2) * np.sin(y) * (x - y)

def df4_dy(x, y):
    return np.exp(-(x - y)**2) * np.cos(y) + 2 * np.exp(-(x - y)**2) * np.sin(y)*(x - y)

# uncomment the following lines for 2D optimization
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ani = optimize2d(f3, df3_dx, df3_dy, -10, 10, -10, 10, 3, 3)
# ani = optimize2d(f4, df4_dx, df4_dy, -np.pi, np.pi, -np.pi, np.pi, 0, 0)

plt.show()