# PyTorch

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
podman build -t snippets-pytorch:latest .
```

### Run a script using the Podman image

On CPU:

```
./run-cpu.sh hello.py
```

On GPU:

```
./run-gpu.sh hello.py
```

#### Podman GPU prerequisites

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


#### Reference documentation

- [Installing Podman and the NVIDIA Container Toolkit](https://docs.nvidia.com/ai-enterprise/deployment/rhel-with-kvm/latest/podman.html#testing-podman-and-nvidia-container-runtime)
- [Installing the NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- [Nvidia - Container Device Interface](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/cdi-support.html)
- [CNCF - The Container Device Interface reference](https://github.com/cncf-tags/container-device-interface)
