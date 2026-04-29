#!/usr/bin/env python3

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# API_URL = "http://localhost:8080/v1"
API_URL = "http://host.containers.internal:8080/v1"  # Use this URL when this script is run within a devcontainer and vLLM is served in a Podman container

model = ChatOpenAI(
    base_url=API_URL,
    api_key="",         # vLLM does not require an API key, but the OpenAI class requires this parameter, so we can just pass an empty string
    model="Qwen/Qwen3-0.6B",
)

messages = [
    SystemMessage(content="Tu es un assistant utile et concis."),
    HumanMessage(content="Explique-moi ce qu'est un LLM en 3 phrases."),
]

response = model.invoke(messages)
print(response.content)
