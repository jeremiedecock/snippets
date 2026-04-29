#!/usr/bin/env python3

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

# API_URL = "http://localhost:8080/v1"
API_URL = "http://host.containers.internal:8080/v1"  # Use this URL when this script is run within a devcontainer and vLLM is served in a Podman container

class AnswerWithJustification(BaseModel):
    '''An answer to the user's question along with a justification for the answer.'''
    answer: str
    '''Answer to the user's question.'''
    justification: str
    '''Justification for the answer.'''

model = ChatOpenAI(
    base_url=API_URL,
    api_key="",         # vLLM does not require an API key, but the OpenAI class requires this parameter, so we can just pass an empty string
    model="Qwen/Qwen3-0.6B",
)

structured_model = model.with_structured_output(AnswerWithJustification)

response = structured_model.invoke("What weighs more, a pound of feathers or a pound of bricks?")
print(response)
