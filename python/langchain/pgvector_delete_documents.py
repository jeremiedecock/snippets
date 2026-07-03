#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# - https://github.com/langchain-ai/langchain-postgres/
# - [PGVector integration - Docs by LangChain](https://docs.langchain.com/oss/python/integrations/vectorstores/pgvector)
# - [PGVector | langchain_postgres | LangChain Reference](https://reference.langchain.com/python/langchain-postgres/vectorstores/PGVector)

from langchain_core.documents import Document
from langchain_mistralai import MistralAIEmbeddings
from langchain_postgres import PGVector

from secret import DBHOST, DBNAME, DBUSER, DBPASSWORD, DBPORT

embeddings_model = MistralAIEmbeddings(model="mistral-embed")

# See docker command above to launch a postgres instance with pgvector enabled.
connection = f"postgresql+psycopg://{DBUSER}:{DBPASSWORD}@{DBHOST}:{DBPORT}/{DBNAME}"
store = PGVector(
    embeddings=embeddings_model,  # No embeddings needed for deletion
    # collection_name="my_documents_collection",
    connection=connection,
)

# Delete all documents in the vector store
store.delete(ids=["79995216-40b7-4149-b6a7-b3829ef93ead"])