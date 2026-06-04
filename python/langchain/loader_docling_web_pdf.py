#!/usr/bin/env python3

# Src : https://docs.langchain.com/oss/python/integrations/document_loaders/docling

"""
Install the langchain-docling package:

```bash
pip install langchain-docling
```
"""

from langchain_docling.loader import DoclingLoader

FILE_PATH = "https://arxiv.org/pdf/2408.09869"

loader = DoclingLoader(file_path=FILE_PATH)
pages = loader.load()

print(pages)
