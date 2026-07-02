#!/usr/bin/env python3

from langchain_core.documents import Document

TEXT = """Hello, this is a sample text that will be converted into a Document object."""

doc = Document(TEXT)

print(doc)
print(doc.page_content)