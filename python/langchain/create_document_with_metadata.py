#!/usr/bin/env python3

from langchain_core.documents import Document

TEXT = """Hello, this is a sample text that will be converted into a Document object."""

METADATA = {"source": "example", "author": "Claude"}

doc = Document(page_content=TEXT, metadata=METADATA)

print(doc)
