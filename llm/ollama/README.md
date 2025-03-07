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

## Open WebUI with Ollama in Podman

```
podman pod create --name ollamapod -p 11434:11434 -p 3000:8080

podman run -d --pod ollamapod -v ollama:/root/.ollama --name ollama docker.io/ollama/ollama
podman exec -it ollama ollama list
# Pull models if required...

podman run -d --pod ollamapod -e WEBUI_AUTH=False -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main
```

Then go to http://localhost:3000/admin/settings and configure the ollama connexion as explained in https://docs.openwebui.com/getting-started/quick-start/starting-with-ollama/
