#!/usr/bin/env python3

# Src : https://github.com/langchain-ai/learning-langchain/tree/master/ch2/py

# **Note**
# WebBaseLoader is a basic web page loader (fetches HTML and parses it with BeautifulSoup).
# Since langchain-community was sunset (May 2026), there is no dedicated standalone package
# for it yet. Two recommended alternatives:
#
# 1. Implement it directly using requests + BeautifulSoup + langchain_core's Document class:
#
#    import requests
#    from bs4 import BeautifulSoup
#    from langchain_core.documents import Document
#
#    response = requests.get('https://www.langchain.com/')
#    soup = BeautifulSoup(response.text, 'html.parser')
#    docs = [Document(page_content=soup.get_text(), metadata={"source": 'https://www.langchain.com/'})]
#
# 2. Use a standalone package with web scraping support:
#    - langchain-unstructured (UnstructuredURLLoader) — advanced parsing
#    - langchain-docling (DoclingLoader) — supports URLs

"""
Install the beautifulsoup4 package:

```bash
pip install beautifulsoup4
```
"""

from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader('https://www.langchain.com/')
docs = loader.load()

print(docs)
