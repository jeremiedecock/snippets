#!/usr/bin/env python3

from langchain_core.prompts import ChatPromptTemplate

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
