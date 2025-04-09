#!/usr/bin/env python3

# Documentation:
# - https://huggingface.co/blog/langchain
# - https://python.langchain.com/docs/integrations/providers/huggingface/

from langchain_huggingface.embeddings import HuggingFaceEmbeddings

model_name = "mixedbread-ai/mxbai-embed-large-v1"

hf_embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
)

texts = ["Hello, world!", "How are you?"]
output = hf_embeddings.embed_documents(texts)

print(f"Input: {texts}\nOutput: {output}")

