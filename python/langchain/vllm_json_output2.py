#!/usr/bin/env python3

# C.f. https://docs.langchain.com/oss/python/langchain/models#structured-output

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# API_URL = "http://localhost:8080/v1"
API_URL = "http://host.containers.internal:8080/v1"  # Use this URL when this script is run within a devcontainer and vLLM is served in a Podman container


class Actor(BaseModel):
    name: str
    role: str

class Movie(BaseModel):
    """A movie with details."""
    title: str = Field(description="The title of the movie")
    year: int = Field(description="The year the movie was released")
    cast: list[Actor] = Field(description="The main cast of the movie")
    director: str = Field(description="The director of the movie")
    rating: float = Field(description="The movie's rating out of 10")


model = ChatOpenAI(
    base_url=API_URL,
    api_key="",         # vLLM does not require an API key, but the OpenAI class requires this parameter, so we can just pass an empty string
    model="Qwen/Qwen3-0.6B",
)
model_with_structure = model.with_structured_output(Movie, include_raw=True)

response = model_with_structure.invoke("Provide details about the movie Inception", max_tokens=128)
print(response)  # Movie(title="Inception", year=2010, director="Christopher Nolan", rating=8.8)
