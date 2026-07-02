#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# - https://github.com/langchain-ai/langchain-postgres/
# - [PGVector integration - Docs by LangChain](https://docs.langchain.com/oss/python/integrations/vectorstores/pgvector)
# - [PGVector | langchain_postgres | LangChain Reference](https://reference.langchain.com/python/langchain-postgres/vectorstores/PGVector)

from langchain_core.documents import Document
from langchain_mistralai import MistralAIEmbeddings
from langchain_postgres.vectorstores import PGVector

from secret import DBHOST, DBNAME, DBUSER, DBPASSWORD, DBPORT


# Make the document ###########################################################

documents = [
    Document(page_content="Apples and oranges"),
    Document(page_content="Cars and airplanes"),
    Document(page_content="Train")
]


# Instantiate the embeddings model ############################################

embeddings_model = MistralAIEmbeddings(model="mistral-embed")


# Store embeddings in PGVector ################################################

# See docker command above to launch a postgres instance with pgvector enabled.
connection = f"postgresql+psycopg://{DBUSER}:{DBPASSWORD}@{DBHOST}:{DBPORT}/{DBNAME}"
collection_name = "my_documents_collection"  # You can choose a name for your collection

store = PGVector(
    embeddings=embeddings_model,
    collection_name=collection_name,
    connection=connection,
    use_jsonb=True,
)

store.add_documents(documents)


# Query the vector store ######################################################

query = "I'd like a fruit."
docs = store.similarity_search(
    query,
    k=1    # Number of results to return. Defaults to 4.
)
print(docs)


query = "I'd like a bike."
docs = store.similarity_search(
    query,
    k=1    # Number of results to return. Defaults to 4.
)
print(docs)