#!/usr/bin/env python3

# Src : https://github.com/langchain-ai/learning-langchain/tree/master/ch2/py

# Note:
# PyPDFLoader is a basic PDF loader that uses the pypdf library.
# Since langchain-community was sunset (May 2026), there is no dedicated standalone package
# for it yet. Two recommended alternatives with standalone packages:
#
# 1. langchain-unstructured (UnstructuredLoader) — advanced parsing, many file types:
#    pip install langchain-unstructured
#    from langchain_unstructured import UnstructuredLoader
#
# 2. langchain-docling (DoclingLoader) — supports PDFs and many other formats:
#    pip install langchain-docling
#    from langchain_docling.loader import DoclingLoader

"""
Install the pypdf package:

```bash
pip install pypdf
```
"""

from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader('./test.pdf')
pages = loader.load()

print(pages)
