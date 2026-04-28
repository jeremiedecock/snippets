#!/bin/bash

# Remarque: `-e VLLM_CPU_KVCACHE_SPACE=8` limite le KV cache à 8 Go

podman run \
    --rm \
    --name=vllm-cpu \
    -v hf-cache:/root/.cache/huggingface \
    --ipc=host \
    -p 8080:8000 \
    -e VLLM_CPU_KVCACHE_SPACE=8 \
    localhost/snippets-vllm-cpu vllm serve --model Qwen/Qwen3-0.6B
