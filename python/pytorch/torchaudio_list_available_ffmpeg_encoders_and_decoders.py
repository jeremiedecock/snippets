#!/usr/bin/env python3

# Doc : https://docs.pytorch.org/audio/stable/generated/torchaudio.utils.ffmpeg_utils.html#torchaudio.utils.ffmpeg_utils.get_audio_decoders

import torchaudio

print("Available FFMPEG encoders:", torchaudio.utils.ffmpeg_utils.get_audio_encoders())
print()
print("Available FFMPEG decoders:", torchaudio.utils.ffmpeg_utils.get_audio_decoders())