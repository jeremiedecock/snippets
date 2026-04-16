#!/usr/bin/env python3

# Documentation: https://huggingface.co/apple/OpenELM-270M-Instruct

# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text-generation", model="apple/OpenELM-270M-Instruct", trust_remote_code=True)