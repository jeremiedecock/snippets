#!/usr/bin/env python3

# https://huggingface.co/google/gemma-4-E2B-it

from transformers import pipeline

MODEL_ID = "google/gemma-4-E2B-it"

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