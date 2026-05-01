# LangChain

- https://python.langchain.com/docs/introduction/
- https://python.langchain.com/docs/tutorials/llm_chain/
- https://python.langchain.com/docs/integrations/chat/huggingface/


## Installation

### PyTorch configuration

Before installing the dependencies, edit `requirements.txt` to select the appropriate PyTorch variant:

- **CPU only**: uncomment the `torch --index-url https://download.pytorch.org/whl/cpu` line and comment out the GPU lines.
- **GPU (CUDA)**: uncomment the line matching your installed CUDA version (e.g. `cu124` for CUDA 12.4, `cu126` for CUDA 12.6). If you need a specific PyTorch version, pin it explicitly (e.g. `torch==2.6.0`). You can check which CUDA version is available on your system by running `nvidia-smi` or `nvcc --version`. Refer to the [official PyTorch installation guide](https://pytorch.org/get-started/locally/) for the full list of supported CUDA versions.

### Install dependencies

From this directory:

```
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```


## Usage

...

## API Keys

### OpenAI

Create an API key on https://platform.openai.com/
and write it in the `OPENAI_API_KEY` environment variable (or in the `.devcontainer/.env` file if using the Dev Container).

### Anthropic Claude

Create an API key on https://platform.claude.com/ and write it in the `ANTHROPIC_API_KEY` environment variable (or in the `.devcontainer/.env` file if using the Dev Container).

### Google Gemini

Create an API key on https://ai.google.dev/api and write it in the `GOOGLE_API_KEY` environment variable (or in the `.devcontainer/.env` file if using the Dev Container).

### Mistral

Create an API key on https://console.mistral.ai/ (c.f. https://docs.mistral.ai/getting-started/quickstarts/developer/first-api-request) and write it in the `MISTRAL_API_KEY` environment variable (or in the `.devcontainer/.env` file if using the Dev Container).


## VS Code Dev Container

### Enable or disable GPU support

To control whether the Dev Container can access Nvidia GPUs, edit `.devcontainer/devcontainer.json` and comment or uncomment the two lines below inside the `"runArgs"` array:

```jsonc
"--device",
"nvidia.com/gpu=all"
```

- **Enable GPU**: leave those two lines uncommented.
- **Disable GPU** (CPU-only): comment them out so the container starts without any GPU device.

After changing this setting, rebuild the container (VS Code command: **Dev Containers: Rebuild Container**) for it to take effect.

> **Warning — Podman required as the container engine**
>
> The `--device nvidia.com/gpu=all` syntax relies on CDI (Container Device Interface), which is a Podman feature. It will **not** work with Docker.
>
> To configure VS Code to use Podman instead of Docker, open the VS Code settings (File › Preferences › Settings, or `Ctrl+,`), search for **"docker path"**, and set **Dev › Containers: Docker Path** (`dev.containers.dockerPath`) to `podman`.
>
> If you are using Docker as the container engine, you must replace the `--device` option with the Docker/NVIDIA equivalent (e.g. `--gpus all` via the NVIDIA Container Toolkit for Docker).

See the [Run a script using the Podman image on Nvidia GPUs](#run-a-script-using-the-podman-image-on-nvidia-gpus) section below for details on how to set up GPU support in Podman via the CDI (Container Device Interface).


## Podman (Linux only)

### Build the Podman image

```
./build.sh
```

or

```
podman build -t snippets-langchain:latest .
```

### Run a script using the Podman image on CPU

```
./run.sh hello.py
```

or 

```
podman run --rm -it -v .:/app -w /app -u $(id -u):$(id -g) --userns=keep-id localhost/snippets-langchain:latest python3 hello.py
```

### Run a script using the Podman image on Nvidia GPUs

#### Prerequisites

To enable GPU support in Podman, ensure NVIDIA Drivers are properly installed on the host.

*Nvidia container toolkit* is also required to run GPU workloads in Podman. Install it using the following commands (Debian/Ubuntu):

```
apt install nvidia-container-toolkit
```

Generate the CDI specification file in `/etc/cdi/nvidia.yaml` (this step must be repeated every time you update the GPU driver or Linux kernel):

```
nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml
```

This command creates a CDI (Container Device Interface) configuration file used by Podman to access GPU devices.

List available GPU devices (optional):

```
nvidia-ctk cdi list
```

You’ll see a list of devices like:

```
nvidia.com/gpu:0
nvidia.com/gpu:1
...
```

These names will be used in the `--device` option when running containers.

#### Run a script using the Podman image on Nvidia GPUs

Execute a snippet on GPU:

```
./run-gpu.sh hello.py
```

or 

```
podman run --rm -it -v .:/app -w /app -u $(id -u):$(id -g) --userns=keep-id --device nvidia.com/gpu=all localhost/snippets-langchain:latest python3 hello_gpu.py
```

Note:
- Replace `--device nvidia.com/gpu=all` with specific GPU IDs (e.g., `nvidia.com/gpu=0`) if needed.
- Use the names listed in `nvidia-ctk cdi list` to ensure compatibility with your setup.


#### Reference documentation

- [Installing Podman and the NVIDIA Container Toolkit](https://docs.nvidia.com/ai-enterprise/deployment/rhel-with-kvm/latest/podman.html#testing-podman-and-nvidia-container-runtime)
- [Installing the NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- [Nvidia - Container Device Interface](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/cdi-support.html)
- [CNCF - The Container Device Interface reference](https://github.com/cncf-tags/container-device-interface)