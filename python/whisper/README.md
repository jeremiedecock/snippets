# OpenAI Whisper

C.f.

- https://github.com/openai/whisper
- https://openai.com/research/whisper
- [Vidéo de Korben "Retranscrire de l'audio / vidéo facilement avec l'IA de Whisper"](https://www.youtube.com/watch?v=3AhOl2q-TW4)


```
pip install -U openai-whisper
sudo apt update && sudo apt install ffmpeg
whisper "your_file.mp3" --model small
```

# Available models

Size     Parameters  English-only model  Multilingual model  Required VRAM   Relative speed
tiny     39 M        tiny.en             tiny                ~1 GB           ~32x
base     74 M        base.en             base                ~1 GB           ~16x
small    244 M       small.en            small               ~2 GB           ~6x
medium   769 M       medium.en           medium              ~5 GB           ~2x
large    1550 M      N/A                 large               ~10 GB          1x
large-v2 ?           ?                   ?                   ?               ?
