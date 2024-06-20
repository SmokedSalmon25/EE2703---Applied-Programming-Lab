# providing necessary imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# defining a function for calculating total distance for a given order
def distance (cities, cityorder):
    totaldistance = 0
    for i in range(len(cities)):
        totaldistance += np.sqrt(((cities[cityorder[i]][0] - cities[cityorder[i-1]][0]) ** 2) + ((cities[cityorder[i]][1] - cities[cityorder[i-1]][1]) ** 2))
    return totaldistance

name = input("Enter the file name: ")
cities = []
file_path = name 
# opening file in read mode
with open(file_path, "r") as file:
    flag = 0
    # Iterate through each line in the file
    for line in file:
        if flag == 0:
            num_cities = int(line)
            flag = 1
        else:
            # converting each line to tuple of x and y coordinates
            city = line.split()
            city = [float(element) for element in city]
            city = np.array(city, dtype = 'float')
            cities.append(city)
cities = np.array(cities)

def tsp(cities):
    # Hyperparameters
    T = 2000
    decayrate = 0.99
    num_epochs = 50000

    order = np.arange(num_cities)
    np.random.shuffle(order)
    bestcost = distance(cities, order)
    initialcost = bestcost
    for epoch in range (num_epochs):
        # Randomly select two distinct indices
        index1, index2 = np.random.choice(num_cities, 2, replace=False)

        # Swap the elements at the selected indices
        order[index1], order[index2] = order[index2], order[index1]
        cost = distance (cities, order)
        if cost < bestcost:
            bestcost = cost
        else:
            toss = np.random.random_sample()
            if toss < np.exp(-(cost-bestcost)/T):
                bestcost = cost
            else:
                order[index1], order[index2] = order[index2], order[index1]
        T = T * decayrate
        print(round(epoch/(num_epochs - 1) * 100, 2), '%', end = '\r')

    print(f"Final optimal path is {order}")
    finalcost = distance(cities, order)
    print(f"The optimized distance is {finalcost}")
    print(f"Percentage improvement is {(initialcost - finalcost)/ initialcost * 100}%")
    return order

# Creating the list of x and y coordinates
x_cities = [element[0] for element in cities]
y_cities = [element[1] for element in cities]
x_cities = np.array(x_cities)
y_cities = np.array(y_cities)
finalorder = tsp(cities)

# Rearrange for plotting
xplot = x_cities[finalorder] 
yplot = y_cities[finalorder]

# To ensure it goes back to original point
xplot = np.append(xplot, xplot[0])
yplot = np.append(yplot, yplot[0])

# Plotting the final graph
plt.plot(xplot, yplot, 'o-')
plt.savefig("Final_path.png")