#!/usr/bin/env python3

from langchain_core.output_parsers import CommaSeparatedListOutputParser

parser = CommaSeparatedListOutputParser()
items = parser.parse("apple, banana, cherry")

print(items)  # ['apple', 'banana', 'cherry']
