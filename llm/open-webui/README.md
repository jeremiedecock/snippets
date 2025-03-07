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

```
podman pod create --name ollamapod -p 11434:11434 -p 3000:8080

podman run -d --pod ollamapod -v ollama:/root/.ollama --name ollama docker.io/ollama/ollama
podman exec -it ollama ollama list
# Pull models if required...

podman run -d --pod ollamapod -e WEBUI_AUTH=False -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main
```

Then go to http://localhost:3000/admin/settings and configure the ollama connexion as explained in https://docs.openwebui.com/getting-started/quick-start/starting-with-ollama/
