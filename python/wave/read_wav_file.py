#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Read the content of an audio wave file (.wav)
# See: https://docs.python.org/3/library/wave.html

import wave

wr = wave.open("./test.wav", mode="rb")

print(wr.readframes(20))   # Read the 20 first frames

print("Num channels:", wr.getnchannels())
print("Sample width:", wr.getsampwidth())
print("Frame rate:", wr.getframerate())
print("Num frames:", wr.getnframes())

wr.close()
