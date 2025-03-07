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
```

to disable authentication.
