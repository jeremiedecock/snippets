# Ollama

## With Podman

```
podman run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama docker.io/ollama/ollama
```

then

```
podman exec -it ollama ollama run phi4-mini
podman exec -it ollama ollama run mistral
podman exec -it ollama ollama run deepseek-r1
```

Stop:

```
podman stop ollama
```

# CLI

See https://github.com/ollama/ollama?tab=readme-ov-file#cli-reference

# Available models

See https://github.com/ollama/ollama?tab=readme-ov-file#model-library

# Custom models (Modelfile)

https://github.com/ollama/ollama?tab=readme-ov-file#customize-a-model
