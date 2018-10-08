#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See http://people.csail.mit.edu/hubert/pyaudio/docs/#example-blocking-mode-audio-i-o

import pyaudio

p = pyaudio.PyAudio()

print("Num devices:", p.get_device_count())
print()

# See https://stackoverflow.com/q/20760589
for i in range(p.get_device_count()):
    print(p.get_device_info_by_index(i))
