#!/usr/bin/env python3

# Src: https://github.com/langchain-ai/learning-langchain/tree/master/ch2/py

# C.f.: https://docs.langchain.com/oss/python/integrations/embeddings/sentence_transformers

from langchain_huggingface import HuggingFaceEmbeddings

# model = HuggingFaceEmbeddings(model="sentence-transformers/all-mpnet-base-v2")  # 110M parameters, Classic, small, CPU-friendly, no prompt required
model = HuggingFaceEmbeddings(model="BAAI/bge-m3")                                # 570M parameters, Multilingual; produces dense, sparse, and multi-vector embeddings in one pass
# model = HuggingFaceEmbeddings(model="Qwen/Qwen3-Embedding-0.6B")                # 595M parameters, Multilingual, instruction-aware, top MTEB performance

embeddings = model.embed_documents([
    "Hi there!",
    "Oh, hello!",
    "What's your name?",
    "My friends call me World",
    "Hello World!"
])

print(embeddings)
