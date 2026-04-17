#!/bin/bash

podman run \
    --rm \
    --name=vllm \
    --device nvidia.com/gpu=all \
    -v hf-cache:/root/.cache/huggingface \
    --ipc=host \
    --env HF_HUB_ENABLE_HF_TRANSFER=0 \
    --env HF_HUB_DISABLE_XET=1 \
    --env VLLM_ENABLE_CUDA_COMPATIBILITY=1 \
    -p 8080:8000 \
    docker.io/vllm/vllm-openai:v0.8.5 --model Qwen/Qwen3-0.6B
