#!/usr/bin/env python3

# https://docs.langchain.com/oss/python/integrations/providers/google#google-generative-ai-gemini-api-and-vertex-ai
# https://ai.google.dev/api

import getpass
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import os

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    # temperature=1.0,  # Gemini 3.0+ defaults to 1.0
    # max_tokens=None,
    # timeout=None,
    # max_retries=2,
    # other params...
)

prompt = [
    SystemMessage(content="Tu es un assistant utile et concis."),
    HumanMessage(content="Explique-moi ce qu'est un LLM en 3 phrases."),
]

response = model.invoke(prompt)
print(response.content)
