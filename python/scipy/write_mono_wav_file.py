#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Read the content of an audio wave file (.wav)
# See: http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.io.wavfile.write.html

import numpy as np
from scipy.io import wavfile

def sin_wave(freq, num_frames, rate):
    data_list = [int(127 * (np.sin(t/float(rate) * freq * 2. * np.pi) + 1)) for t in range(num_frames)]
    return np.array(data_list, dtype=np.int8)

rate = 24000
num_frames = 48000

nparray = sin_wave(440, num_frames, rate)

wavfile.write("./test.wav", rate, nparray)
