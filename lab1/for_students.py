import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv

from data import get_data, inspect_data, split_data, linear_function

data = get_data()
#inspect_data(data)

train_data, test_data = split_data(data)

# Simple Linear Regression
# predict MPG (y, dependent variable) using Weight (x, independent variable) using closed-form solution
# y = theta_0 + theta_1 * x - we want to find theta_0 and theta_1 parameters that minimize the prediction error

# We can calculate the error using MSE metric:
# MSE = SUM (from i=1 to n) (actual_output - predicted_output) ** 2

# get the columns
y_train = train_data['MPG'].to_numpy()
x_train = train_data['Weight'].to_numpy()


y_test = test_data['MPG'].to_numpy()
x_test = test_data['Weight'].to_numpy()



# TODO: calculate closed-form solution
#theta_best = [0, 0]

x_train_col = x_train.reshape(-1, 1)
y_train_col = y_train.reshape(-1, 1)
ones_col = np.ones((len(x_train), 1)) # ilosc rzedow x dlugosc rzedu
observation_matrix = np.concatenate((ones_col, x_train_col), axis=1) # macierz obserwacji z jednej cechy

step_one = np.matmul(observation_matrix.T, observation_matrix)   #X^t * X

step_two = np.dot(inv(step_one), observation_matrix.T)  #(X^t * X)^-1  * X^t

vector_theta = np.dot(step_two, y_train_col)

theta_best = vector_theta.flatten()

print(theta_best)



# TODO: calculate error


y_train_predict = observation_matrix.dot(theta_best)
mse_train = np.mean((y_train_predict - y_train) ** 2)

print(mse_train)


# plot the regression line
x = np.linspace(min(x_test), max(x_test), 100)
y = float(theta_best[0]) + float(theta_best[1]) * x
plt.plot(x, y, color='red')
plt.scatter(x_test, y_test)
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.show()

# TODO: standardization

x_train_mean = np.mean(x_train)
x_train_std = np.std(x_train)

x_train_standardized = (x_train - x_train_mean) / x_train_std
x_test_standardized = (x_test - x_train_mean) / x_train_std

ones_col_standarized = np.ones((len(x_train_standardized), 1)) # ilosc rzedow x dlugosc rzedu
bias = np.concatenate((ones_col, x_train_col), axis=1) # macierz obserwacji z jednej cechy

print(bias)



# TODO: calculate theta using Batch Gradient Descent

# TODO: calculate error

# plot the regression line
x = np.linspace(min(x_test), max(x_test), 100)
y = float(theta_best[0]) + float(theta_best[1]) * x
plt.plot(x, y, color='red')
plt.scatter(x_test, y_test)
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.show()