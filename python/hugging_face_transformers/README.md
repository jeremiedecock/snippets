# HuggingFace Transformers

See: https://github.com/huggingface/transformers


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
podman build -t snippets-hf-transformers:latest .
```

### Run a script using the Podman image

```
./run.sh python3 smollm2-135m-instruct.py
```

or 

```
podman run --rm -it -v .:/app -w /app -u $(id -u):$(id -g) --userns=keep-id localhost/snippets-hf-transformers:latest python3 smollm2-135m-instruct.py
```

To use Nvidia GPUs with Podman, check https://docs.nvidia.com/ai-enterprise/deployment/rhel-with-kvm/latest/podman.html#testing-podman-and-nvidia-container-runtime

### Transformers Chat CLI

```
podman run --rm -it localhost/snippets-hf-transformers:latest transformers-cli chat --model_name_or_path HuggingFaceTB/SmolLM2-135M-Instruct
```
