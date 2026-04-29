#!/usr/bin/env python3

# C.f. https://docs.langchain.com/oss/python/langchain/models#structured-output

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

class AnswerWithJustification(BaseModel):
    '''An answer to the user's question along with a justification for the answer.'''
    answer: str
    '''Answer to the user's question.'''
    justification: str
    '''Justification for the answer.'''

model = ChatOpenAI()
structured_model = model.with_structured_output(AnswerWithJustification)

response = structured_model.invoke("What weighs more, a pound of feathers or a pound of bricks?")
print(response)
