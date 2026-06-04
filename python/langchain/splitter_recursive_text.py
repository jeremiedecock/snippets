#!/usr/bin/env python3

# Src : https://github.com/langchain-ai/learning-langchain/tree/master/ch2/py

# C.f.
# - https://github.com/langchain-ai/langchain/tree/master/libs/text-splitters#readme
# - https://reference.langchain.com/python/langchain-text-splitters
# - https://reference.langchain.com/python/langchain-text-splitters/character/RecursiveCharacterTextSplitter
# - https://reference.langchain.com/python/langchain-text-splitters/base/TextSplitter


from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

loader = TextLoader('./test.txt', encoding="utf-8")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size=100,
    chunk_overlap=20,
)
splitted_docs = splitter.split_documents(docs)

for doc in splitted_docs:
    print(f"\n{doc}\n")