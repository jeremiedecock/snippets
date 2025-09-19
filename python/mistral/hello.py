#!/usr/bin/env python3

# Documentation:
# - https://docs.mistral.ai/getting-started/quickstart/#getting-started-with-mistral-ai-api

import os
from mistralai import Mistral

import tomllib

with open("secrets.toml", "rb") as f:
    data = tomllib.load(f)

api_key = data['mistral_api_key']
model = "mistral-small-2503"

client = Mistral(api_key=api_key)

chat_response = client.chat.complete(
    model= model,
    messages = [
        {
            "role": "user",
            "content": "What is the best French cheese?",
        },
    ]
)

print(chat_response.choices[0].message.content)
