#!/usr/bin/env python3

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate


# Make the prompt #####################

template = [
    ("system", "You are a helpful assistant. You respond to questions in {language}."),
    ("human", "What is the capital of {country}?")
]

chat_prompt_template = ChatPromptTemplate.from_messages(template)

prompt = chat_prompt_template.invoke({
    "language": "French",
    "country": "France"
})

print(prompt.to_string())


# Invoke the model ####################

# API_URL = "http://localhost:8080/v1"
API_URL = "http://host.containers.internal:8080/v1"  # Use this URL when this script is run within a devcontainer and vLLM is served in a Podman container

model = ChatOpenAI(
    base_url=API_URL,
    api_key="",         # vLLM does not require an API key, but the OpenAI class requires this parameter, so we can just pass an empty string
    model="Qwen/Qwen3-0.6B",
)

response = model.invoke(prompt)
print(response.content)
