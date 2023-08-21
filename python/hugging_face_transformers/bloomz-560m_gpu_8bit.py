#!/usr/bin/env python3

# Source: https://huggingface.co/bigscience/bloomz-560m#gpu

# Model "bigscience/bloomz-560m" (560M parameters): multitask finetuned on xP3.
# Recommended for prompting in English. 
# See: https://huggingface.co/bigscience/bloomz-560m

from transformers import AutoTokenizer, AutoModelForCausalLM

checkpoint = "bigscience/bloomz-560m"

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint, device_map="auto", load_in_8bit=True)

inputs = tokenizer.encode("Translate to English: Je t’aime.", return_tensors="pt").to("cuda")
outputs = model.generate(inputs)

print(tokenizer.decode(outputs[0]))
