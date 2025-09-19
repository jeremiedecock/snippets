# LangChain

- https://docs.mistral.ai/getting-started/


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

## OpenAI API Key

Create an API key on https://console.mistral.ai/api-keys
and write it in the key in the `secrets.toml` file.

## Podman

### Build the Podman image

```
./build.sh
```

or

```
podman build -t snippets-mistral:latest .
```

### Run a script using the Podman image on CPU

```
./run.sh hello.py
```

or 

```
podman run --rm -it -v .:/app -w /app -u $(id -u):$(id -g) --userns=keep-id localhost/snippets-mistral:latest python3 hello.py
```
