# Gradio

See: https://www.gradio.app/


## Installation

From this directory:

```
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

## Usage

...

## Podman

See https://www.gradio.app/guides/deploying-gradio-with-docker

### Build the Podman image

```
./build.sh
```

or

```
podman build -t snippets-gradio:latest .
```

### Run a script using the Podman image

```
./run.sh gradio hello.py
```

or 

```
podman run --rm -it -p 7860:7860 -v .:/app -w /app -u $(id -u):$(id -g) --userns=keep-id localhost/snippets-gradio:latest gradio hello.py
```

To use Nvidia GPUs with Podman, check https://docs.nvidia.com/ai-enterprise/deployment/rhel-with-kvm/latest/podman.html#testing-podman-and-nvidia-container-runtime

