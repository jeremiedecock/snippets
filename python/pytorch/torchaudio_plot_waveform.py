#!/usr/bin/env python3

# Doc :
# - https://docs.pytorch.org/audio/stable/generated/torchaudio.transforms.Spectrogram.html#torchaudio.transforms.Spectrogram
# - https://docs.pytorch.org/audio/stable/tutorials/audio_feature_extractions_tutorial.html#sphx-glr-tutorials-audio-feature-extractions-tutorial-py

import torch
import torchaudio
import matplotlib.pyplot as plt

# Fetch the audio file

audio_file = torchaudio.utils.download_asset("tutorial-assets/Lab41-SRI-VOiCES-src-sp0307-ch127535-sg0042.wav")

audio_tensor, sample_rate = torchaudio.load(audio_file)

print("Tensor shape:", audio_tensor.shape)
print("Sample rate:", sample_rate)

# Plot the waveform

waveform = audio_tensor.numpy()

num_channels, num_frames = waveform.shape
time_axis = torch.arange(0, num_frames) / sample_rate

plt.figure(figsize=(10, 4))
plt.plot(time_axis, waveform[0], linewidth=1)
plt.grid(True)
plt.xlim([0, time_axis[-1]])
plt.title("Waveform")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()

plt.savefig("torchaudio_plot_waveform.png", dpi=300, bbox_inches="tight")
plt.close()