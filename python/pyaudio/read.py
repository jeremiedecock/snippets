#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See http://people.csail.mit.edu/hubert/pyaudio/docs/#example-blocking-mode-audio-i-o

import pyaudio
import wave

CHUNK = 1024

wf = wave.open("test.wav", 'rb')

print(wf.getnchannels())
print(wf.getframerate())

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                output_device_index=3)

# read data
data = wf.readframes(CHUNK)

while len(data) > 0:
    stream.write(data)
    data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()

p.terminate()
