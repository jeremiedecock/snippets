#!/usr/bin/env python3

from langchain_core.prompts import PromptTemplate

template = "What is the capital of {country}?"

prompt_template = PromptTemplate.from_template(template)

print(prompt_template.invoke({"country": "France"}))
