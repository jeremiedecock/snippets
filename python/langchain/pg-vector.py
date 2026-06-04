#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# conn = psycopg2.connect(
#     host=DBHOST,
#     database=DBNAME,
#     user=DBUSER,
#     password=DBPASSWORD,
# )

# cur = conn.cursor()

from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres.vectorstores import PGVector
from langchain_core.documents import Document
import psycopg2
import uuid

from secret import DBHOST, DBNAME, DBUSER, DBPASSWORD, DBPORT


# See docker command above to launch a postgres instance with pgvector enabled.
# connection = f"postgresql+psycopg://langchain:langchain@localhost:{DBPORT}/langchain"

connection = psycopg2.connect(
    host=DBHOST,
    database=DBNAME,
    user=DBUSER,
    password=DBPASSWORD,
)

# Load the document, split it into chunks
raw_documents = TextLoader('./test.txt', encoding="utf-8").load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
documents = text_splitter.split_documents(raw_documents)

# Create embeddings for the documents
embeddings_model = HuggingFaceEmbeddings(model="BAAI/bge-m3")

db = PGVector.from_documents(
    documents,
    embeddings_model,
    connection=connection
)

results = db.similarity_search("query", k=4)

# print(results)

# print("Adding documents to the vector store")
# ids = [str(uuid.uuid4()), str(uuid.uuid4())]
# db.add_documents(
#     [
#         Document(
#             page_content="there are cats in the pond",
#             metadata={"location": "pond", "topic": "animals"},
#         ),
#         Document(
#             page_content="ducks are also found in the pond",
#             metadata={"location": "pond", "topic": "animals"},
#         ),
#     ],
#     ids=ids,
# )

# print("Documents added successfully.\n Fetched documents count:",
#       len(db.get_by_ids(ids)))

# print("Deleting document with id", ids[1])
# db.delete({"ids": ids})

# print("Document deleted successfully.\n Fetched documents count:",
#       len(db.get_by_ids(ids)))