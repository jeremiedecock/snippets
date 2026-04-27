#!/bin/bash

podman run \
    --rm \
    --name=vllm-cpu \
    -v hf-cache:/root/.cache/huggingface \
    --ipc=host \
    -p 8080:8000 \
    localhost/snippets-vllm-cpu vllm serve --model "HuggingFaceTB/SmolLM2-135M"
