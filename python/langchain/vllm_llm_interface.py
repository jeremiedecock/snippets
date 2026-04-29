#!/usr/bin/env python3

from langchain_openai import OpenAI

# API_URL = "http://localhost:8080/v1"
API_URL = "http://host.containers.internal:8080/v1"  # Use this URL when this script is run within a devcontainer and vLLM is served in a Podman container

model = OpenAI(
    base_url=API_URL,
    api_key="",         # vLLM does not require an API key, but the OpenAI class requires this parameter, so we can just pass an empty string
    model="Qwen/Qwen3-0.6B",
    # temperature=0.7,
    # max_tokens=128,
)

response = model.invoke("The capital of France is")
print(response)
