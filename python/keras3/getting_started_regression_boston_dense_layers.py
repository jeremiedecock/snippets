#!/usr/bin/env python3
# coding: utf-8

# Sources:
# - "L'apprentissage Profond avec Python" de François Chollet. Ed. Manning. P.112-120
# - Fidle seq. 1: https://www.youtube.com/watch?v=aJHB9TadgAg&t=701s

import keras
from aim.keras import AimCallback

print(f"Keras version {keras.__version__}")


# Prepare the data ############################################################

# Load the data and split it between train and test sets
(x_train, y_train), (x_test, y_test) = keras.datasets.boston_housing.load_data()

# Normalize features
mean = x_train.mean(axis=0)
std = x_train.std(axis=0)

x_train = (x_train - mean) / std
x_test = (x_test - mean) / std

#pd.DataFrame(x_train).plot.hist()
#plt.show()

#pd.DataFrame(x_test).plot.hist()
#plt.show()

# Build the model #############################################################

model = keras.Sequential([
    keras.layers.Input(shape=(x_train.shape[1],),               name="InputLayer"),
    keras.layers.Dense(units=64,          activation="relu",    name="Dense_1"),
    keras.layers.Dense(units=64,          activation="relu",    name="Dense_2"),
    keras.layers.Dense(units=1,           activation="linear",  name="Output"),
])

model.summary()


# Train the model #############################################################

model.compile(loss="mse", optimizer="adam", metrics=["mae"])

print("\n# Fit", "#" * (80-5), "\n")
model.fit(x_train, y_train, batch_size=128, epochs=200, validation_split=0.1, callbacks=[AimCallback(experiment='Boston Housing')])


# Evaluate the trained model ##################################################

print("\n# Evaluate", "#" * (80-12), "\n")
score = model.evaluate(x_test, y_test, verbose=0)

print(f"Test loss (MSE): {score[0]}")
print(f"Test metric (MAE): {score[1]}\n")


# Predict an example ##########################################################

for i in range(5):
    print("# Predict", "#" * (80-12), "\n")
    prediction = model.predict(x_test[i:i+1])

    print(f"\nPredicted: {prediction}")
    print(f"Expected: {y_test[i]}\n")