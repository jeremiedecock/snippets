#!/usr/bin/env python3

# Documentation:
# - https://huggingface.co/blog/langchain
# - https://python.langchain.com/docs/integrations/providers/huggingface/

from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline

llm = HuggingFacePipeline.from_model_id(
    model_id="HuggingFaceTB/SmolLM2-135M-Instruct",
    task="text-generation",
    pipeline_kwargs={
        "max_new_tokens": 100,
        "top_k": 50,
        "do_sample": True,
        "temperature": 0.1,
    },
)

llm_engine_hf = ChatHuggingFace(llm=llm)

# Test de génération de texte

prompt = "HuggingFace is"
output = llm_engine_hf.invoke(prompt)

print(f"Input: {prompt}\nOutput: {output}")

