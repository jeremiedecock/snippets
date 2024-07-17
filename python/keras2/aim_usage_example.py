#!/usr/bin/env python3
# coding: utf-8

# Source: https://aimstack.readthedocs.io/en/latest/quick_start/integrations.html#integration-with-keras-tf-keras

from tensorflow import keras
import numpy as np


# Enable Aim ##################################################################

# call keras as the high api of tensorflow
#from aim.tensorflow import AimCallback
# call keras library directly
from aim.keras import AimCallback


# Prepare the data ############################################################

# Load the data and split it between train and test sets
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Convert class vectors to binary class matrices
num_classes = 10
input_shape = (28, 28, 1)

# Scale images to the [0, 1] range
x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255

# Make sure images have shape (28, 28, 1)
# Change x_train.shape from (60000, 28, 28) to (60000, 28, 28, 1)
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)

# Convert class vectors to binary class matrices (i.e. use the "one-hot encoding")
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)


# Build the model #############################################################

model = keras.Sequential(
    [
        keras.layers.Input(shape=input_shape),
        keras.layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        keras.layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        keras.layers.Flatten(),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(num_classes, activation="softmax"),
    ]
)

model.summary()


# Train the model #############################################################

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

print("\n\n" + "*"*80)
print("Type this in another therminal: aim up")
print("and open in your web browser the printed URL (e.g. http://127.0.0.1:43800/)")
print("*"*80, "\n\n")

model.fit(x_train, y_train, batch_size=128, epochs=15, validation_split=0.1, callbacks=[AimCallback(experiment='aim_on_keras')])


# Evaluate the trained model ##################################################

score = model.evaluate(x_test, y_test, verbose=0)
print("\nTest loss:", score[0])
print("Test accuracy:", score[1])