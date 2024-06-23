#!/usr/bin/env python3

# This script print the name of the current Keras 3 backend

import keras

print()
print(f"Keras version: {keras.__version__}")
print(f"Backend name: {keras.backend.backend()}")
print()