#!/usr/bin/env python3

# Src: https://github.com/langchain-ai/learning-langchain/tree/master/ch2/py

# C.f.:
# - https://reference.langchain.com/python/langchain-core/embeddings/embeddings/Embeddings
# - https://docs.langchain.com/oss/python/integrations/embeddings/mistralai

from langchain_mistralai import MistralAIEmbeddings

model = MistralAIEmbeddings(model="mistral-embed")

TEXT = "Hi there!"

embedding = model.embed_query(TEXT)

print(embedding)