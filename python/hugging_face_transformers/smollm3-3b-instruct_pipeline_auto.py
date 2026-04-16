#!/usr/bin/env python3

# https://huggingface.co/HuggingFaceTB/SmolLM3-3B

from transformers import pipeline

MODEL_ID = "HuggingFaceTB/SmolLM3-3B"

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