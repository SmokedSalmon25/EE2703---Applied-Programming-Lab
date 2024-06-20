#making the necessary imports
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Opening the dataset and reading in the space separated input
csvfile = open('Admission_Predict_Ver1.1.csv', 'r')
csvreader = csv.reader(csvfile, delimiter = ',')

#reading in the data and converting into numpy array
data = []
Chance = []
flag = 0
for row in csvreader:
    if flag == 0:
        flag = 1
    else:
        data.append(row[1:-1])
        Chance.append(row[8])
data = np.asarray(data, 'float64')
Chance = np.asarray(Chance, 'float64')

#normalizing the data
for i in range (len(data)):
    data[i][0] = data[i][0] / 340
    data[i][1] = data[i][1] / 120
    data[i][2] = data[i][2] / 5
    data[i][3] = data[i][3] / 5
    data[i][4] = data[i][4] / 5
    data[i][5] = data[i][5] / 10 
data = data.T

#defining a linear model to perform curve fit
def model(x, a, b, c, d, e, f, g, h):
    return a + b * (x[0]) + c * (x[1]) + d * ((1 / x[2])) + e * (x[3]) + f * (x[4]) + g * (x[5]) + h * (x[6])
bounds = ([-np.inf, 0, 0, 0, 0, 0, 0, 0], [np.inf, np.inf, np.inf, np.inf, np.inf,np.inf, np.inf, np.inf])
params, _ = curve_fit(model, data, Chance, bounds = bounds)
y_pred_lin = model(data, params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7])
lin_error = np.average(abs((y_pred_lin - Chance)/Chance * 100))
print(f"The percentage error in the linear case is {lin_error}%")

#defining a non linear model to perform curve_fit
def model(x, a, b, c, d, e, f, g, h, p1, p2, p3, p4, p5, p6):
    return a + b * (x[0] ** p1) + c * (x[1] ** p2) + d * ((1 / x[2]) ** p3) + e * (x[3] ** p4) + f * (x[4] ** p5) + g * (x[5] ** p6) + h * (x[6])
bounds = ([-np.inf, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf])
params, _ = curve_fit(model, data, Chance, bounds = bounds)
y_pred_non_lin = model(data, params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8], params[9], params[10], params[11], params[12], params[13])
non_lin_error = np.average(abs((y_pred_non_lin - Chance)/Chance * 100))
print(f"The percentage error in the non linear case is {non_lin_error}%")
