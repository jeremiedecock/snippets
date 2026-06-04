#!/usr/bin/env python3

# Src: https://github.com/langchain-ai/learning-langchain/tree/master/ch2/py

# C.f.: https://docs.langchain.com/oss/python/integrations/embeddings/cohere

from langchain_cohere import CohereEmbeddings

model = CohereEmbeddings(model="embed-english-v3.0")

embeddings = model.embed_documents([
    "Hi there!",
    "Oh, hello!",
    "What's your name?",
    "My friends call me World",
    "Hello World!"
])

print(embeddings)
