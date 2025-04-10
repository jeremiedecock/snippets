#!/usr/bin/env python3

from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

model = ChatOpenAI()

system_msg = SystemMessage("Your are a helpful assistant that responds to questions with three exclamation marks.")
human_msg = HumanMessage("What is the capital of France?")

prompt = [system_msg, human_msg]
output = model.invoke(prompt)

print(f"Input: {prompt}\nOutput: {output}")

