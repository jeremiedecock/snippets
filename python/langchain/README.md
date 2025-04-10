# LangChain

- https://python.langchain.com/docs/introduction/
- https://python.langchain.com/docs/tutorials/llm_chain/
- https://python.langchain.com/docs/integrations/chat/huggingface/


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

Create an API key on https://platform.openai.com/
and write it in the `OPENAI_API_KEY` environment variable.

## Podman

### Build the Podman image

```
./build.sh
```

or

```
podman build -t snippets-langchain:latest .
```

### Run a script using the Podman image

```
./run.sh hello.py
```

or 

```
podman run --rm -it -v .:/app -w /app -u $(id -u):$(id -g) --userns=keep-id localhost/snippets-langchain:latest python3 hello.py
```

To use Nvidia GPUs with Podman, check https://docs.nvidia.com/ai-enterprise/deployment/rhel-with-kvm/latest/podman.html#testing-podman-and-nvidia-container-runtime

