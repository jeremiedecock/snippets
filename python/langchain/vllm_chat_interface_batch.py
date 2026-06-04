#!/usr/bin/env python3

from langchain_openai import ChatOpenAI

# API_URL = "http://localhost:8080/v1"
API_URL = "http://host.containers.internal:8080/v1"  # Use this URL when this script is run within a devcontainer and vLLM is served in a Podman container

model = ChatOpenAI(
    base_url=API_URL,
    api_key="no-key-required",  # vLLM does not require an API key, but the OpenAI class requires a non-empty value
    model="Qwen/Qwen3-0.6B",
)

responses = model.batch([
    "What is the capital of France?",
    "What is the capital of Germany?",
])

for response in responses:
    print(response.content)
    print()
