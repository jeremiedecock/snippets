#!/usr/bin/env python3
# coding: utf-8

# Source: "L'apprentissage Profond avec Python" de François Chollet. Ed. Manning. P.93-95

from tensorflow import keras
import numpy as np


# Prepare the data ############################################################

# Load the data and split it between train and test sets
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Keep only the first two classes to make a binary classification problem #####
train_selected_idx = (y_train==0)|(y_train==1)
x_train = x_train[train_selected_idx]
y_train = y_train[train_selected_idx]

test_selected_idx = (y_test==0)|(y_test==1)
x_test = x_test[test_selected_idx]
y_test = y_test[test_selected_idx]

# Check the new dataset #######################################################
#for i in range(20):
#    print(y_train[i])
#    plt.imshow(x_train[i], cmap="gray")
#    plt.show()
#
#for i in range(20):
#    print(y_test[i])
#    plt.imshow(x_test[i], cmap="gray")
#    plt.show()

# Convert class vectors to binary class matrices
input_shape = (28, 28)

# Scale images to the [0, 1] range
x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255

# Convert class vectors to float vectors
y_train = y_train.astype("float32")
y_test = y_test.astype("float32")


# Build the model #############################################################

model = keras.Sequential([
    keras.layers.Input(shape=input_shape,                name="InputLayer"),
    keras.layers.Flatten(),
    keras.layers.Dense(units=64,   activation="relu",    name="Dense_1"),
    keras.layers.Dense(units=64,   activation="relu",    name="Dense_2"),
    keras.layers.Dense(units=1,    activation="sigmoid", name="Output"),
])

model.summary()


# Train the model #############################################################

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

print("\n# Fit", "#" * (80-5), "\n")
model.fit(x_train, y_train, batch_size=128, epochs=5, validation_split=0.1)


# Evaluate the trained model ##################################################

print("\n# Evaluate", "#" * (80-12), "\n")
score = model.evaluate(x_test, y_test, verbose=0)

print(f"Test loss: {score[0]}")
print(f"Test accuracy: {score[1]}\n")


# Predict an example ##########################################################

for i in range(5):
    #plt.imshow(x_test[i], cmap="gray")
    #plt.show()

    print("# Predict", "#" * (80-12), "\n")
    prediction = model.predict(x_test[i:i+1])

    print(f"\nPredicted raw output: {prediction}")

    print(f"Predicted class: {prediction.round()}")
    print(f"Actual class: {y_test[i]}\n")
