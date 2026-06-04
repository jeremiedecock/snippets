#!/usr/bin/env python3

# Src : https://github.com/langchain-ai/learning-langchain/tree/master/ch2/py

# **Note**
# TextLoader is a basic file reader with no external dependencies. Since langchain-community
# was sunset (May 2026), there is no dedicated standalone package for it yet. The recommended
# approach is to implement it directly using langchain_core's Document class, or to keep using
# langchain_community.document_loaders as long as it remains functional (no longer maintained).
from langchain_community.document_loaders import TextLoader

loader = TextLoader('./test.txt', encoding="utf-8")
docs = loader.load()

print(docs)
