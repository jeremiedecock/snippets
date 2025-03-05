#!/usr/bin/env python3

# https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct

from transformers import AutoModelForCausalLM, AutoTokenizer

checkpoint = "HuggingFaceTB/SmolLM2-360M-Instruct"

device = "cpu" # "cuda" for GPU usage

tokenizer = AutoTokenizer.from_pretrained(checkpoint)

# for multiple GPUs install accelerate and do `model = AutoModelForCausalLM.from_pretrained(checkpoint, device_map="auto")`
model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)

messages = [{"role": "user", "content": "What is gravity?"}]

input_text=tokenizer.apply_chat_template(messages, tokenize=False)
print(input_text)

inputs = tokenizer.encode(input_text, return_tensors="pt").to(device)
outputs = model.generate(inputs, max_new_tokens=500, temperature=0.2, top_p=0.9, do_sample=True)

print(tokenizer.decode(outputs[0]))

