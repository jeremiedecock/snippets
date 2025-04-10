#!/usr/bin/env python3

from langchain_openai.llms import OpenAI

model = OpenAI(model="gpt-4o-mini-2024-07-18")

prompt = "The sky is"
output = model.invoke(prompt)

print(f"Input: {prompt}\nOutput: {output}")

