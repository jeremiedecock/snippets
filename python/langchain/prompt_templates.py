#!/usr/bin/env python3

from langchain_core.prompts import PromptTemplate

template = "What is the capital of {country}?"

template = PromptTemplate.from_template(template)

print(template.invoke({"country": "France"}))
