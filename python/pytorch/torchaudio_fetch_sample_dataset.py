#!/usr/bin/env python3

# Doc :
# - https://docs.pytorch.org/audio/stable/tutorials/audio_feature_extractions_tutorial.html#sphx-glr-tutorials-audio-feature-extractions-tutorial-py
# - https://docs.pytorch.org/audio/stable/generated/torchaudio.info.html#torchaudio.info

import torchaudio

audio_file = torchaudio.utils.download_asset("tutorial-assets/Lab41-SRI-VOiCES-src-sp0307-ch127535-sg0042.wav")

print(audio_file)
print(type(audio_file))

print(torchaudio.info(audio_file))