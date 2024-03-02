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

x_test_col = x_test.reshape(-1, 1)
ones_col_test = np.ones((len(x_test_col), 1))
observation_matrix_test = np.concatenate((ones_col_test, x_test_col), axis=1)

y_test_predict = observation_matrix_test.dot(theta_best)



y_train_predict = observation_matrix.dot(theta_best)
mse_train = np.mean((y_train_predict - y_train) ** 2)
mse_test = np.mean((y_test_predict - y_test) ** 2)

print(f"mse train: {mse_train}")
print(f"mse test: {mse_test}")

#print(mse_train)


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

y_train_mean = np.mean(y_train)
y_train_std = np.std(y_train)

x_train_standardized = (x_train - x_train_mean) / x_train_std
x_test_standardized = (x_test - x_train_mean) / x_train_std

y_train_standardized = (y_train - y_train_mean) / y_train_std
y_test_standardized = (y_test - y_train_mean) / y_train_std



ones_col_standarized = np.ones((len(x_train_standardized), 1)) # ilosc rzedow x dlugosc rzedu


x_train_standardized = x_train_standardized.reshape(-1, 1)
y_train_standardized = y_train_standardized.reshape(-1, 1)

observation_matrix_standarized = np.concatenate((ones_col_standarized, x_train_standardized), axis=1) # macierz obserwacji z jednej cechy

#print(observation_matrix_standarized)



# TODO: calculate theta using Batch Gradient Descent

LEARNING_RATE = 0.01
ITERATIONS = 1000
theta_best = np.random.rand(2,1) # wartosci theta z przedzialu 0, 1

print(f"random init thetas {theta_best.flatten()}")
for iteration in range(ITERATIONS):
      gradient = 2/len(x_train_col) * observation_matrix_standarized.T.dot(observation_matrix_standarized.dot(theta_best) - y_train_standardized)
      theta_best = theta_best - LEARNING_RATE * gradient


theta_best = theta_best.flatten()
print(f"found thetas {theta_best}")
# TODO: calculate error



x_test_standardized = x_test_standardized.reshape(-1, 1)
ones_col_test = np.ones((len(x_test_standardized), 1))


observation_matrix_standarized_test = np.concatenate((ones_col_test, x_test_standardized), axis=1)

y_train_predict = observation_matrix_standarized.dot(theta_best)
y_test_predict = observation_matrix_standarized_test.dot(theta_best)

mse_train = np.mean((y_train_predict - y_train_standardized) ** 2)
mse_test = np.mean((y_test_predict - y_test_standardized) ** 2)

print(mse_train, mse_test)


# plot the regression line
x = np.linspace(min(x_test_standardized), max(x_test_standardized), 100)
y = float(theta_best[0]) + float(theta_best[1]) * x
plt.plot(x, y, color='red')
plt.scatter(x_test_standardized, y_test_standardized)
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.show()