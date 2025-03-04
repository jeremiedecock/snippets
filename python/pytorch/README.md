# Installation

## Posix (Linux, MacOSX, WSL, ...)

From this directory:

```
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

# Podman

## Build the Podman image

```
./build.sh
```

or

```
podman build -t snippets-pytorch:latest .
```

## Run a script using the Podman image

```
./run.sh ./hello_cuda.py
```

or 

```
podman run --rm -it -v .:/app -w /app -u $(id -u):$(id -g) --userns=keep-id localhost/snippets-pytorch:latest python3 ./hello_cuda.py
```

To use Nvidia GPUs with Podman, check https://docs.nvidia.com/ai-enterprise/deployment/rhel-with-kvm/latest/podman.html#testing-podman-and-nvidia-container-runtime
