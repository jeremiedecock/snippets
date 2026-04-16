#!/usr/bin/env python3

# https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct

from transformers import pipeline

MODEL_ID = "HuggingFaceTB/SmolLM2-135M-Instruct"

# Load pipeline
pipe = pipeline(
    "text-generation",
    model=MODEL_ID,
    device_map="auto",
)

# Prompt
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Write a short joke about saving RAM."},
]

# Generate output
result = pipe(messages)

print(result)