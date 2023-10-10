#!/usr/bin/env python3

# Source: https://huggingface.co/stabilityai/stablelm-3b-4e1t

from transformers import AutoModelForCausalLM, AutoTokenizer
import os

tokenizer = AutoTokenizer.from_pretrained("stabilityai/stablelm-3b-4e1t", token=os.environ.get("HUGGINGFACE_API_TOKEN"))

model = AutoModelForCausalLM.from_pretrained(
  "stabilityai/stablelm-3b-4e1t",
  trust_remote_code=True,
  torch_dtype="auto",
)

model.cuda()

inputs = tokenizer("The weather is always wonderful", return_tensors="pt").to("cuda")
tokens = model.generate(
  **inputs,
  max_new_tokens=64,
  temperature=0.75,
  top_p=0.95,
  do_sample=True,
)

print(tokenizer.decode(tokens[0], skip_special_tokens=True))