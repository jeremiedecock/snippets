#!/usr/bin/env python3

# Documentation:
# - https://huggingface.co/blog/langchain
# - https://python.langchain.com/docs/integrations/providers/huggingface/

from langchain_huggingface import HuggingFacePipeline

model = HuggingFacePipeline.from_model_id(model_id="HuggingFaceTB/SmolLM2-135M-Instruct", task="text-generation")
output = model.invoke("The sky is")

print(output)
