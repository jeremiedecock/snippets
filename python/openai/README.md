# OpenAI

- https://platform.openai.com/docs/quickstart


## Installation

From this directory:

```
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements-minimal.txt
```

C.f. https://platform.openai.com/docs/libraries?language=python

## OpenAI API Key

Create an API key on https://platform.openai.com/
and write it in the `OPENAI_API_KEY` environment variable.

## Podman

### Build the Podman image

```
./build.sh
```

or

```
podman build -t snippets-openai:latest .
```

### Run a script using the Podman image

```
./run.sh hello.py
```

or 

```
podman run --rm -it -v .:/app -w /app -u $(id -u):$(id -g) --userns=keep-id localhost/snippets-openai:latest python3 hello.py
```

To use Nvidia GPUs with Podman, check https://docs.nvidia.com/ai-enterprise/deployment/rhel-with-kvm/latest/podman.html#testing-podman-and-nvidia-container-runtime

