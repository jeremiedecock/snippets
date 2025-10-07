# OpenAI Whisper

C.f.

- https://huggingface.co/openai/whisper-large-v3
- https://github.com/openai/whisper
- https://openai.com/research/whisper
- [Vidéo de Korben "Retranscrire de l'audio / vidéo facilement avec l'IA de Whisper"](https://www.youtube.com/watch?v=3AhOl2q-TW4)


# Available models

Size     Parameters  English-only model  Multilingual model  Required VRAM   Relative speed
tiny     39 M        tiny.en             tiny                ~1 GB           ~32x
base     74 M        base.en             base                ~1 GB           ~16x
small    244 M       small.en            small               ~2 GB           ~6x
medium   769 M       medium.en           medium              ~5 GB           ~2x
large    1550 M      N/A                 large               ~10 GB          1x
large-v2 1550 M      ?                   ?                   ?               ?
large-v3 1550 M      ?                   ?                   ?               ?

Rem: downloaded models are stored in `./.cache`


# Installation

## Posix (Linux, MacOSX, WSL, ...)

From this directory:

```
sudo apt update && sudo apt install ffmpeg
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

# Usage

## Transript a file

```
whisper "your_file.mp3" --model small
```

The following audio files can be used to test Whisper: https://commons.wikimedia.org/wiki/Category:Audio_files

## Live transcript (micro)

```
./whisper_live.py
```


# Podman

## Build the Podman image

```
./build.sh
```

or

```
podman build -t snippets-whisper:latest .
```

## Run a script using the Podman image

E.g. for `apollo11.ogg`:

```
./run.sh whisper apollo11.ogg --model small
```

or 

```
podman run --rm -it -v .:/app -w /app -u $(id -u):$(id -g) --userns=keep-id localhost/snippets-whisper:latest whisper apollo11.ogg --model small
```

The following audio files can be used to test Whisper: https://commons.wikimedia.org/wiki/Category:Audio_files

To use Nvidia GPUs with Podman, check https://docs.nvidia.com/ai-enterprise/deployment/rhel-with-kvm/latest/podman.html#testing-podman-and-nvidia-container-runtime


## Run a script using the Podman image on a GPU

With the "large-v3" model:

```
./run-gpu.sh whisper --model large-v3 apollo11.ogg
```

or With the default "turbo" model:

```
./run-gpu.sh whisper apollo11.ogg
```

## Tips

Video files can be provided directly:

```
./run-gpu.sh whisper video.mp4
```

Caution: when using whisper with Podman, input files have to be in the current directory, otherwise they won't be in a mounted volume in the container.
