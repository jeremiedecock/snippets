#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wave

wr = wave.open("./test.wav", mode="rb")

print(wr.readframes(20))   # Read the 20 first frames

print("Num channels:", wr.getnchannels())
print("Sample width:", wr.getsampwidth())
print("Frame rate:", wr.getframerate())
print("Num frames:", wr.getnframes())

wr.close()
