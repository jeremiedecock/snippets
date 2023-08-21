#!/usr/bin/env python3

# Source: https://huggingface.co/bigscience/mt0-small#cpu

# Model "bigscience/mt0-small" (300M parameters): multitask finetuned on xP3.
# Recommended for prompting in English. 
# See: https://huggingface.co/bigscience/mt0-small

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

checkpoint = "bigscience/mt0-small"

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

inputs = tokenizer.encode("Translate to English: Je t’aime.", return_tensors="pt")
outputs = model.generate(inputs)

print(tokenizer.decode(outputs[0]))
