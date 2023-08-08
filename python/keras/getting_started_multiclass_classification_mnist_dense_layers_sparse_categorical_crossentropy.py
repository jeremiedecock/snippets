#!/usr/bin/env python3
# coding: utf-8

# Source: Fidle seq. 1
# - https://gricad-gitlab.univ-grenoble-alpes.fr/talks/fidle/-/blob/master/MNIST/01-DNN-MNIST.ipynb
# - https://www.youtube.com/watch?v=aJHB9TadgAg&t=701s

from tensorflow import keras
import numpy as np


# Prepare the data ############################################################

# Load the data and split it between train and test sets
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Convert class vectors to binary class matrices
num_classes = 10
input_shape = (28, 28)

# Scale images to the [0, 1] range
x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255


# Build the model #############################################################

model = keras.Sequential([
    keras.layers.Input(shape=input_shape,                       name="InputLayer"),
    keras.layers.Flatten(),
    keras.layers.Dense(units=64,          activation="relu",    name="Dense_1"),
    keras.layers.Dense(units=64,          activation="relu",    name="Dense_2"),
    keras.layers.Dense(units=num_classes, activation="softmax", name="Output"),
])

model.summary()


# Train the model #############################################################

model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

print("\n# Fit", "#" * (80-5), "\n")
model.fit(x_train, y_train, batch_size=128, epochs=5, validation_split=0.1)


# Evaluate the trained model ##################################################

print("\n# Evaluate", "#" * (80-12), "\n")
score = model.evaluate(x_test, y_test, verbose=0)

print(f"Test loss: {score[0]}")
print(f"Test accuracy: {score[1]}\n")


# Predict an example ##########################################################

for i in range(5):
    print("# Predict", "#" * (80-12), "\n")
    prediction = model.predict(x_test[i:i+1])

    print(f"\nPredicted raw output: {prediction}")

    print(f"Predicted class: {prediction.argmax()}")
    print(f"Actual class: {y_test[i]}\n")
