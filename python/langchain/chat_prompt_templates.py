#!/usr/bin/env python3

from langchain_core.prompts import ChatPromptTemplate

template = [
    ("system", "You are a helpful assistant."),
    ("human", "What is the capital of {country}?")
]

template = ChatPromptTemplate.from_messages(template)

print(template.invoke({"country": "France"}))
