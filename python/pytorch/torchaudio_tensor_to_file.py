#!/usr/bin/env python3

# Doc :
# - https://docs.pytorch.org/audio/stable/generated/torchaudio.save.html#torchaudio.save

import torchaudio

# Load the audio file

audio_file = torchaudio.utils.download_asset("tutorial-assets/Lab41-SRI-VOiCES-src-sp0307-ch127535-sg0042.wav")

audio_tensor, sample_rate = torchaudio.load(audio_file)

print("Tensor shape:", audio_tensor.shape)
print("Sample rate:", sample_rate)

# Save the tensor to a file

torchaudio.save("output.wav", audio_tensor, sample_rate)

print("Tensor saved to output.wav")