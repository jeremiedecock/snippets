#!/usr/bin/env python3

# C.f. https://docs.langchain.com/oss/python/langchain/models#structured-output

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# API_URL = "http://localhost:8080/v1"
API_URL = "http://host.containers.internal:8080/v1"  # Use this URL when this script is run within a devcontainer and vLLM is served in a Podman container


# Note: we use `Field(description=...)` rather than per-attribute "docstrings"
# (i.e. bare string literals placed under each annotated attribute, like in the
# commented-out version below).
#
# Reasons:
#   1. Python only treats the first string literal in a class body as a real
#      docstring (the class docstring). String literals placed after attribute
#      annotations are just no-op expressions; they are NOT exposed as
#      docstrings at runtime and have no official status in the language.
#   2. Pydantic v2 does not extract these attribute "docstrings" by default,
#      so they would not appear as `description` entries in the generated JSON
#      schema -- and therefore would never be sent to the LLM when calling
#      `model.with_structured_output(AnswerWithJustification)`.
#   3. `Field(description=...)` is the explicit, portable and well-supported
#      way to attach a description to each field. Pydantic includes it in the
#      JSON schema, which LangChain forwards to the model so it knows exactly
#      what each field is meant to contain.
#
# Equivalent (but ineffective) version using attribute "docstrings":
#
# class AnswerWithJustification(BaseModel):
#     '''An answer to the user's question along with a justification for the answer.'''
#     answer: str
#     '''Answer to the user's question.'''
#     justification: str
#     '''Justification for the answer.'''

class AnswerWithJustification(BaseModel):
    '''An answer to the user's question along with a justification for the answer.'''
    answer: str = Field(description="Answer to the user's question.")
    justification: str = Field(description="Justification for the answer.")

model = ChatOpenAI(
    base_url=API_URL,
    api_key="",         # vLLM does not require an API key, but the OpenAI class requires this parameter, so we can just pass an empty string
    model="Qwen/Qwen3-0.6B",
)

structured_model = model.with_structured_output(AnswerWithJustification)

response: AnswerWithJustification = structured_model.invoke("What weighs more, a pound of feathers or a pound of bricks?")
print(response)
print()

print("Response is instance of AnswerWithJustification?", isinstance(response, AnswerWithJustification))  # True
print()

print(f"JSON:\n{ response.model_dump_json(indent=2) }")
print()

print(f"Answer:\n{ response.answer }\n\nJustification:\n{ response.justification }")