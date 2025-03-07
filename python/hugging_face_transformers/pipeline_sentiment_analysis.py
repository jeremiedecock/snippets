#!/usr/bin/env python3

# https://huggingface.co/docs/transformers/quicktour

from transformers import pipeline

classifier = pipeline("sentiment-analysis")
result = classifier("We are very happy to show you the 🤗 Transformers library.")

print(result)
