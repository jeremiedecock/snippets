# HuggingFace Transformers

See:
- https://huggingface.co/docs/trl/main/en/index
- https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct#chat-in-trl

## Installation

From this directory:

```
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements-minimal.txt
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
podman build -t snippets-hf-trl:latest .
```

### Run a script using the Podman image

```
./run.sh trl chat --model_name_or_path HuggingFaceTB/SmolLM2-135M-Instruct --device cpu
```

or 

```
podman run --rm -it -v .:/app -w /app -u $(id -u):$(id -g) --userns=keep-id localhost/snippets-hf-transformers:latest trl chat --model_name_or_path HuggingFaceTB/SmolLM2-135M-Instruct --device cpu
```

To use Nvidia GPUs with Podman, check https://docs.nvidia.com/ai-enterprise/deployment/rhel-with-kvm/latest/podman.html#testing-podman-and-nvidia-container-runtime

