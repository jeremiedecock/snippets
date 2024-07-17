#!/usr/bin/env python3

import keras
import numpy as np
import matplotlib.pyplot as plt

print(keras.__version__)

(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Print shape of the data
print("x_train.shape:", x_train.shape)
print("y_train.shape:", y_train.shape)
print("x_test.shape:", x_test.shape)
print("y_test.shape:", y_test.shape)

# Print the number of classes
print("Number of classes:", np.unique(y_train).shape[0])

# Plot the first image
plt.imshow(x_train[0], cmap='gray')
plt.show()