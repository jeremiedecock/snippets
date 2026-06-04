#!/usr/bin/env python3

# Src: https://github.com/langchain-ai/learning-langchain/tree/master/ch2/py

# C.f.: https://docs.langchain.com/oss/python/integrations/embeddings/openai

from langchain_openai import OpenAIEmbeddings

model = OpenAIEmbeddings(model="text-embedding-3-small")

embeddings = model.embed_documents([
    "Hi there!",
    "Oh, hello!",
    "What's your name?",
    "My friends call me World",
    "Hello World!"
])

print(embeddings)
