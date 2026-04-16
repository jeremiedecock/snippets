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

On CPU:

```
./run-cpu.sh smollm2-135m-instruct-cpu.py
```

On GPU:

```
./run-gpu.sh smollm2-135m-instruct-gpu.py
```

To use Nvidia GPUs with Podman, check https://docs.nvidia.com/ai-enterprise/deployment/rhel-with-kvm/latest/podman.html#testing-podman-and-nvidia-container-runtime

### Transformers Chat CLI

On CPU:

```
./run-serve-cpu.sh
./run-chat-cli.sh  HuggingFaceTB/SmolLM2-135M-Instruct
podman stop hf-transformers-serve
```

On GPU:

```
./run-serve-gpu.sh
./run-chat-cli.sh  HuggingFaceTB/SmolLM2-135M-Instruct
podman stop hf-transformers-serve
```

You can replace `HuggingFaceTB/SmolLM2-135M-Instruct` with any other model, e.g. `HuggingFaceTB/SmolLM3-3B`.