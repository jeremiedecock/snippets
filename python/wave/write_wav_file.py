#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Read the content of an audio wave file (.wav)
# See: https://docs.python.org/3/library/wave.html

import math
import wave

T = 24000.

def sin_wave(freq, nframes):
    data = [int(127 * (math.sin(t/T * freq * 2. * math.pi) + 1)) for t in range(nframes)]
    return bytes(data)

ww = wave.open("./test2.wav", mode="wb")

ww.setnchannels(1)          # Num channels
ww.setsampwidth(1)          # Sample width
ww.setframerate(int(T))     # Frame rate
#ww.setnframes(20)          # Num frames

data = sin_wave(440, 48000)
ww.writeframes(data)

ww.close()
