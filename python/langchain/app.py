#!/usr/bin/env python3

from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Charger le modèle Hugging Face

#model_name = "EleutherAI/phi-1.5"
model_name = "microsoft/Phi-3.5-mini-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Configurer le pipeline

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_length=50)
llm = HuggingFacePipeline(pipeline=pipe)

# Test de génération de texte

prompt = "Hello, how are you?"
output = llm(prompt)

print(f"Input: {prompt}\nOutput: {output}")

