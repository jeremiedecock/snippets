#!/usr/bin/env python3

from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage

model = ChatOpenAI()

prompt = [HumanMessage("What is the capital of France?")]
output = model.invoke(prompt)

print(f"Input: {prompt}\nOutput: {output}")

