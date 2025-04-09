#!/usr/bin/env python3

# Documentation:
# - https://huggingface.co/blog/langchain
# - https://python.langchain.com/docs/integrations/providers/huggingface/

from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Charger le modèle Hugging Face

model_name = "HuggingFaceTB/SmolLM2-135M-Instruct"
# model_name = "HuggingFaceTB/SmolLM2-360M-Instruct"

device = "cpu" # "cuda" for GPU usage

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

# Configurer le pipeline

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=100,
    top_k=50,
    do_sample=True,
    temperature=0.5
)
llm = HuggingFacePipeline(pipeline=pipe)

# Test de génération de texte

prompt = "HuggingFace is"
output = llm.invoke(prompt)

print(f"Input: {prompt}\nOutput: {output}")

