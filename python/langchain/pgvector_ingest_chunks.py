#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# - https://github.com/langchain-ai/langchain-postgres/
# - [PGVector integration - Docs by LangChain](https://docs.langchain.com/oss/python/integrations/vectorstores/pgvector)
# - [PGVector | langchain_postgres | LangChain Reference](https://reference.langchain.com/python/langchain-postgres/vectorstores/PGVector)

from langchain_community.document_loaders import TextLoader
from langchain_mistralai import MistralAIEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

from secret import DBHOST, DBNAME, DBUSER, DBPASSWORD, DBPORT


# Load the document ###########################################################

loader = TextLoader("./test.txt", encoding="utf-8")
documents = loader.load()


# Split the document ##########################################################

splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
chunks = splitter.split_documents(documents)


# Instantiate the embeddings model ############################################

embeddings_model = MistralAIEmbeddings(model="mistral-embed")


# Store embeddings in PGVector ################################################

connection = f"postgresql+psycopg://{DBUSER}:{DBPASSWORD}@{DBHOST}:{DBPORT}/{DBNAME}"

vector_store = PGVector(embeddings=embeddings_model, connection=connection)
vector_store.add_documents(chunks)