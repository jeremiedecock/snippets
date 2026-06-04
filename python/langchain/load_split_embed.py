#!/usr/bin/env python3

# Src: https://github.com/langchain-ai/learning-langchain/tree/master/ch2/py

# C.f.: https://docs.langchain.com/oss/python/integrations/embeddings/sentence_transformers

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings


# Load the document ###########################################################

loader = TextLoader("./test.txt", encoding="utf-8")
doc = loader.load()


# Split the document ##########################################################

splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
chunks = splitter.split_documents(doc)


# Generate embeddings #########################################################

# embeddings_model = HuggingFaceEmbeddings(model="sentence-transformers/all-mpnet-base-v2")  # 110M parameters, Classic, small, CPU-friendly, no prompt required
embeddings_model = HuggingFaceEmbeddings(model="BAAI/bge-m3")                                # 570M parameters, Multilingual; produces dense, sparse, and multi-vector embeddings in one pass
# embeddings_model = HuggingFaceEmbeddings(model="Qwen/Qwen3-Embedding-0.6B")                # 595M parameters, Multilingual, instruction-aware, top MTEB performance

embeddings = embeddings_model.embed_documents(
    [chunk.page_content for chunk in chunks]
)

print(embeddings)
