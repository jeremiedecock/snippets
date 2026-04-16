#!/usr/bin/env python3

# Documentation: https://huggingface.co/apple/OpenELM-270M-Instruct

# Load model directly
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("apple/OpenELM-270M-Instruct", trust_remote_code=True)