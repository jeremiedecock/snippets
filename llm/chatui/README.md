# Chat-UI

C.f.:
- Config: https://huggingface.co/docs/chat-ui/configuration/models/overview
- Docker: https://huggingface.co/docs/chat-ui/installation/docker
- Src: https://github.com/huggingface/chat-ui
- https://github.com/huggingface/chat-ui/issues/1436#issuecomment-2311711721

# TODO

Local inference -> add `"endpoints": [...]` in `env.local.all` ; See:
- https://huggingface.co/docs/chat-ui/configuration/models/providers/ollama
- https://huggingface.co/docs/chat-ui/configuration/models/providers/tgi

# Usage

## Start

```
podman run --rm -p 8000:3000 -e HF_TOKEN="${HUGGINGFACE_API_TOKEN}" --mount type=bind,source="env.local.all",target=/app/.env.local -v chat-ui:/data --name chat-ui ghcr.io/huggingface/chat-ui-db:latest
```

Open in browser: http://localhost:8000

## Stop

```
podman stop chat-ui ; podman rm chat-ui ; podman volume rm chat-ui
```
