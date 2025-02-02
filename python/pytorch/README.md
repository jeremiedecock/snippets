Installation
============

Posix (Linux, MacOSX, WSL, ...)
-------------------------------

From this directory:

```
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

Podman
======

Build the Podman image:
```
podman build -t pytorch:latest .
```

Run a script using the Podman image:
```
podman run -it -v $(pwd):/app -u $(id -u):$(id -g) localhost/pytorch:latest python3 ./hello_cuda.py
```

To use Nvidia GPUs with Podman, check https://docs.nvidia.com/ai-enterprise/deployment/rhel-with-kvm/latest/podman.html#testing-podman-and-nvidia-container-runtime
