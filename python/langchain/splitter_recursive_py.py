#!/usr/bin/env python3

# Src : https://github.com/langchain-ai/learning-langchain/tree/master/ch2/py

# C.f.
# - https://github.com/langchain-ai/langchain/tree/master/libs/text-splitters#readme
# - https://reference.langchain.com/python/langchain-text-splitters
# - https://reference.langchain.com/python/langchain-text-splitters/character/RecursiveCharacterTextSplitter
# - https://reference.langchain.com/python/langchain-text-splitters/base/TextSplitter


from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

loader = TextLoader('./test.py', encoding="utf-8")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=50,
    chunk_overlap=0,
)
splitted_docs = splitter.split_documents(docs)

print("---\n")
for doc in splitted_docs:
    print(f"{doc}\n\n---\n")