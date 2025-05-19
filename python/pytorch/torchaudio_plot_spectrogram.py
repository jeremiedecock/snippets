#!/usr/bin/env python3

# Doc :
# - https://docs.pytorch.org/audio/stable/generated/torchaudio.transforms.Spectrogram.html#torchaudio.transforms.Spectrogram
# - https://docs.pytorch.org/audio/stable/tutorials/audio_feature_extractions_tutorial.html#sphx-glr-tutorials-audio-feature-extractions-tutorial-py

import torchaudio
import matplotlib.pyplot as plt

# Fetch the audio file

audio_file = torchaudio.utils.download_asset("tutorial-assets/Lab41-SRI-VOiCES-src-sp0307-ch127535-sg0042.wav")

audio_tensor, sample_rate = torchaudio.load(audio_file)

print("Tensor shape:", audio_tensor.shape)
print("Sample rate:", sample_rate)

# Define the transform

transform = torchaudio.transforms.Spectrogram(n_fft=512, power=2.0)  # power=2.0 for amplitude spectrogram, power=1.0 for magnitude spectrogram

# Apply the transform

spectrogram = transform(audio_tensor)

print("Spectrogram shape:", spectrogram.shape)

# Convert an amplitude spectrogram to dB-scaled spectrogram

amplitude_to_db_transform = torchaudio.transforms.AmplitudeToDB(stype="amplitude") # amplitude or maginitude ?
spectrogram_db = amplitude_to_db_transform(spectrogram)

# Plot the spectrogram

plt.figure(figsize=(10, 4))
plt.imshow(spectrogram_db[0], origin="lower", aspect="auto", vmin=-100)  # Set vmin to -100 dB for better visualization
plt.title("Spectrogram")
plt.colorbar(format='%+2.0f dB')
plt.xlabel("Time")
plt.ylabel("Frequency (Hz)")
plt.show()

plt.savefig("torchaudio_plot_spectrogram.png", dpi=300, bbox_inches="tight")
plt.close()