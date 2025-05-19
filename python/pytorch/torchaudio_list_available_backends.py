#!/usr/bin/env python3

# Doc :
# - https://docs.pytorch.org/audio/stable/generated/torchaudio.list_audio_backends.html#torchaudio.list_audio_backends
# - https://docs.pytorch.org/audio/stable/torchaudio.html

import torchaudio

print("Available backends:", torchaudio.list_audio_backends())