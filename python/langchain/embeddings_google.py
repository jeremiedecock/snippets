#!/usr/bin/env python3

# Src: https://github.com/langchain-ai/learning-langchain/tree/master/ch2/py

# C.f.: https://docs.langchain.com/oss/python/integrations/embeddings/google_generative_ai

from langchain_google_genai import GoogleGenerativeAIEmbeddings

model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")

embeddings = model.embed_documents([
    "Hi there!",
    "Oh, hello!",
    "What's your name?",
    "My friends call me World",
    "Hello World!"
])

print(embeddings)
