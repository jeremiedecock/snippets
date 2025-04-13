# HuggingFace Diffusers

See: https://github.com/huggingface/diffusers


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

### Build the Podman image

```
./build.sh
```

or

```
podman build -t snippets-hf-diffusers:latest .
```

### Run a script using the Podman image

```
./run.sh sdxl-turbo_cpu.py
./run.sh sdxl-1.0-base_cpu.py
./run-gpu.sh sdxl-1.0-full_gpu.py
```

or 

```
podman run --rm -it -v .:/app -w /app -u $(id -u):$(id -g) --userns=keep-id localhost/snippets-hf-diffusers:latest python3 sdxl-turbo_cpu.py
```

To use Nvidia GPUs with Podman, check https://docs.nvidia.com/ai-enterprise/deployment/rhel-with-kvm/latest/podman.html#testing-podman-and-nvidia-container-runtime

