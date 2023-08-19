#!/usr/bin/env python3

# Source: https://huggingface.co/bigscience/mt0-small#gpu

# Model "bigscience/mt0-small" (300M parameters): multitask finetuned on xP3.
# Recommended for prompting in English. 
# See: https://huggingface.co/bigscience/mt0-small

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

checkpoint = "bigscience/mt0-small"

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint, torch_dtype="auto", device_map="auto")

inputs = tokenizer.encode("Translate to English: Je t’aime.", return_tensors="pt").to("cuda")
outputs = model.generate(inputs)

print(tokenizer.decode(outputs[0]))
