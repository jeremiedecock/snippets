#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# - https://github.com/langchain-ai/langchain-postgres/
# - https://docs.langchain.com/oss/python/integrations/vectorstores/pgvectorstore
#
# Note: `langchain_postgres.PGVector` is deprecated since `langchain-postgres` v0.0.14.
# This script uses its replacement, `langchain_postgres.PGVectorStore`.

from langchain_core.documents import Document
from langchain_mistralai import MistralAIEmbeddings
from langchain_postgres import PGEngine, PGVectorStore

from secret import DBHOST, DBNAME, DBUSER, DBPASSWORD, DBPORT


# Make the document ###########################################################

documents = [
    Document(page_content="Apples and oranges"),
    Document(page_content="Cars and airplanes"),
    Document(page_content="Train")
]


# Instantiate the embeddings model ############################################

embeddings_model = MistralAIEmbeddings(model="mistral-embed")
VECTOR_SIZE = 1024  # Dimension of the "mistral-embed" embeddings


# Store embeddings in PGVectorStore ###########################################

# See docker command above to launch a postgres instance with pgvector enabled.
connection = f"postgresql+psycopg://{DBUSER}:{DBPASSWORD}@{DBHOST}:{DBPORT}/{DBNAME}"
table_name = "my_documents_collection"  # You can choose a name for your table

engine = PGEngine.from_connection_string(url=connection)

# Create the table if it doesn't already exist. This only needs to be done once.
engine.init_vectorstore_table(
    table_name=table_name,
    vector_size=VECTOR_SIZE,
)

store = PGVectorStore.create_sync(
    engine=engine,
    table_name=table_name,
    embedding_service=embeddings_model,
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