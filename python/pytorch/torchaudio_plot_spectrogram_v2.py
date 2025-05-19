#!/usr/bin/env python3

# Doc :
# - https://docs.pytorch.org/audio/stable/generated/torchaudio.transforms.Spectrogram.html#torchaudio.transforms.Spectrogram
# - https://docs.pytorch.org/audio/stable/tutorials/audio_feature_extractions_tutorial.html#sphx-glr-tutorials-audio-feature-extractions-tutorial-py
# - https://docs.pytorch.org/audio/stable/tutorials/mvdr_tutorial.html#helper-functions

import torch
import torchaudio
import matplotlib.pyplot as plt

# Fetch the audio file

audio_file = torchaudio.utils.download_asset("tutorial-assets/Lab41-SRI-VOiCES-src-sp0307-ch127535-sg0042.wav")

audio_tensor, sample_rate = torchaudio.load(audio_file)

print("Tensor shape:", audio_tensor.shape)
print("Sample rate:", sample_rate)

# Define the transform

transform = torchaudio.transforms.Spectrogram(n_fft=512, power=None)  # power=None for complex spectrogram, power=2.0 for amplitude spectrogram, power=1.0 for magnitude spectrogram

# Apply the transform

stft = transform(audio_tensor)

print("Spectrogram shape:", stft.shape)

# Convert an amplitude spectrogram to dB-scaled spectrogram

magnitude = stft.abs()
spectrogram_db = 20 * torch.log10(magnitude + 1e-8).numpy()

# Plot the spectrogram

plt.figure(figsize=(10, 4))
plt.imshow(spectrogram_db[0], origin="lower", aspect="auto", vmin=-100, vmax=0)  # Set vmin to -100 dB for better visualization
plt.title("Spectrogram")
plt.colorbar(format='%+2.0f dB')
plt.xlabel("Time")
plt.ylabel("Frequency (Hz)")
plt.show()

plt.savefig("torchaudio_plot_spectrogram_v2.png", dpi=300, bbox_inches="tight")
plt.close()