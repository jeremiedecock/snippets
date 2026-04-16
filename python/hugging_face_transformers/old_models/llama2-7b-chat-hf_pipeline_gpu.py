#!/usr/bin/env python3

# Source: https://huggingface.co/meta-llama/Llama-2-7b-chat-hf?library=true

# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text-generation", model="meta-llama/Llama-2-7b-chat-hf")

