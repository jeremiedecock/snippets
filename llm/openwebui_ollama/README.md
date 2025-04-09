# Open WebUI

- https://github.com/open-webui/open-webui?tab=readme-ov-file#quick-start-with-docker-
- https://docs.openwebui.com/getting-started/quick-start (select Podman)
- https://docs.openwebui.com/getting-started/quick-start/starting-with-ollama/
- https://docs.openwebui.com/getting-started/

```
podman run -p 3000:8080 -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main
```

or

```
podman run -p 3000:8080 -e WEBUI_AUTH=False -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main
podman run --network=slirp4netns:allow_host_loopback=true -p 3000:8080 -e WEBUI_AUTH=False -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main
```

to disable authentication.

## Open WebUI with Ollama in Podman

### Using shared Podman network

First, create a shared network:

```
podman network create openwebui-ollama
```

Then, run ollama and open-webui:

```
podman run -d --network openwebui-ollama --name ollama     -p 11434:11434 -v ollama:/root/.ollama docker.io/ollama/ollama
podman exec -it ollama ollama pull gemma3:1b      # If you want to use Gemma3
podman exec -it ollama ollama pull phi4-mini      # If you want to use Phi4 mini
podman exec -it ollama ollama pull mistral        # If you want to use Mistral 7b
podman exec -it ollama ollama pull deepseek-r1    # If you want to use Deepseek R1
podman exec -it ollama ollama pull llama3.2:1b    # If you want to use Llama 3.2
podman exec -it ollama ollama list                # To list available models
podman run -d --network openwebui-ollama --name open-webui -p 3000:8080   -v open-webui:/app/backend/data -e WEBUI_AUTH=False  ghcr.io/open-webui/open-webui:main
```

Then:

1. Go to http://localhost:3000/ (to "authenticate", even if authentication is disabled). If you have an error saying the ressource is unreachable, wait few seconds then retry.
2. Go to http://localhost:3000/admin/settings and configure the Ollama connection (as explained in https://docs.openwebui.com/getting-started/quick-start/starting-with-ollama/):
  - Navigate to "Connections > Manage Ollama API Connections" (click the wrench icon).
  - Change the URL to: `http://ollama:11434`
  - Click the "Verify Connection" button (the two circular arrows to the left of the "on/off" switch).
  - Click the "Save" button.
3. Go back to http://localhost:3000/ to start chatting.

To stop Ollama and OpenWebUI:

```
podman stop ollama open-webui
```

To restart Ollama and OpenWebUI:

```
podman start ollama open-webui
```

To stop and erase everything:

```
podman stop ollama open-webui
podman rm ollama open-webui
podman volume rm ollama open-webui
podman network rm openwebui-ollama
```

### Using Podman pod

First, create a pod:

```
podman pod create --name openwebui-ollama -p 11434:11434 -p 3000:8080
```

Then, run ollama and open-webui:

```
podman run -d --pod openwebui-ollama --name ollama     -v ollama:/root/.ollama docker.io/ollama/ollama
podman exec -it ollama ollama pull gemma3:1b
podman exec -it ollama ollama pull phi4-mini
podman exec -it ollama ollama pull mistral
podman exec -it ollama ollama pull deepseek-r1
podman exec -it ollama ollama pull llama3.2:1b
podman exec -it ollama ollama list
podman run -d --pod openwebui-ollama --name open-webui -v open-webui:/app/backend/data -e WEBUI_AUTH=False ghcr.io/open-webui/open-webui:main
```

Then:
1. Go to http://localhost:3000/ (to "authenticate", even if authentication is disabled).
2. Go to http://localhost:3000/admin/settings and configure the Ollama connection (as explained in https://docs.openwebui.com/getting-started/quick-start/starting-with-ollama/):
  - Navigate to "Connections > Manage Ollama API Connections" (click the wrench icon).
  - Change the URL to: `http://ollama:11434`
  - Click the "Verify Connection" button (the two circular arrows to the left of the "on/off" switch).
  - Click the "Save" button.
3. Go back to http://localhost:3000/ to start chatting.

To stop and erase everything:

```
podman pod stop openwebui-ollama
podman pod rm openwebui-ollama
podman volume rm ollama open-webui
```

