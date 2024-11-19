#!/bin/sh

# C.f.:
# - Config: https://huggingface.co/docs/chat-ui/configuration/models/overview
# - Docker: https://huggingface.co/docs/chat-ui/installation/docker
# - Src: https://github.com/huggingface/chat-ui

# docker run -p 3000:3000 --env-file .env.local -v chat-ui:/data --name chat-ui ghcr.io/huggingface/chat-ui-db
# docker run -p 8000:3000 -e HF_TOKEN="${HUGGINGFACE_API_TOKEN}" -v db:/data                     ghcr.io/huggingface/chat-ui-db:latest
# docker run -p 8000:3000 --env-file .env.local                  -v chat-ui:/data --name chat-ui ghcr.io/huggingface/chat-ui-db

# All
docker run -p 8000:3000 -e HF_TOKEN="${HUGGINGFACE_API_TOKEN}" --mount type=bind,source="$(pwd)/.env.local.all",target=/app/.env.local -v chat-ui:/data --name chat-ui ghcr.io/huggingface/chat-ui-db:latest
# Open in browser: http://localhost:8000

# Default (Hermes3)
docker run -p 8000:3000 -e HF_TOKEN="${HUGGINGFACE_API_TOKEN}" -v chat-ui:/data --name chat-ui ghcr.io/huggingface/chat-ui-db:latest
# Open in browser: http://localhost:8000

# Mistral7b
docker run -p 8000:3000 -e HF_TOKEN="${HUGGINGFACE_API_TOKEN}" --mount type=bind,source="$(pwd)/.env.local.mistral7b",target=/app/.env.local -v chat-ui:/data --name chat-ui ghcr.io/huggingface/chat-ui-db:latest
#docker run -p 3000:3000 --mount type=bind,source="$(pwd)/.env.local",target=/app/.env.local -v chat-ui:/data --name chat-ui ghcr.io/huggingface/chat-ui-db

# C.f.: https://github.com/huggingface/chat-ui/issues/1436#issuecomment-2311711721
docker run -p 8000:3000 --env-file .env.local -v chat-ui:/data --name chat-ui ghcr.io/huggingface/chat-ui-db
# Open in browser: http://localhost:8000

# Stop:
# docker stop chat-ui && docker rm chat-ui && docker volume rm chat-ui