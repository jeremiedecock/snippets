#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Read the content of an audio wave file (.wav)
# See: http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.io.wavfile.read.html

from scipy.io import wavfile

rate, nparray = wavfile.read("./test.wav")

print(nparray)
print("frame rate:", rate)
print("num frames:", nparray.shape[0])
print("num channels:", nparray.shape[1])
print("frame size:", nparray.dtype)
