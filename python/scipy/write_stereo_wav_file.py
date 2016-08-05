#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Read the content of an audio wave file (.wav)
# See: http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.io.wavfile.write.html

import numpy as np
from scipy.io import wavfile

def sin_wave(freq1, freq2, num_frames, rate):
    data_list_1 = [int(127 * (np.sin(t/float(rate) * freq1 * 2. * np.pi) + 1)) for t in range(num_frames)]
    data_list_2 = [int(127 * (np.sin(t/float(rate) * freq2 * 2. * np.pi) + 1)) for t in range(num_frames)]
    data_list = [data_list_1, data_list_2]
    return np.array(data_list, dtype=np.int8).T

rate = 24000
num_frames = 48000

nparray = sin_wave(440, 880, num_frames, rate)

wavfile.write("./test.wav", rate, nparray)
