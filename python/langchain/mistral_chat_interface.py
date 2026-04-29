#!/usr/bin/env python3

# https://docs.langchain.com/oss/python/integrations/providers/mistralai
# https://docs.mistral.ai/getting-started/quickstarts/developer/first-api-request

import getpass
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_mistralai import ChatMistralAI
import os

if "MISTRAL_API_KEY" not in os.environ:
    os.environ["MISTRAL_API_KEY"] = getpass.getpass("Enter your Mistral API key: ")

# Models overview: https://docs.mistral.ai/models/overview
model = ChatMistralAI(
    # model="mistral-large-latest",
    # model="ministral-8b-2512",
    model="mistral-small-2603",
)

prompt = [
    SystemMessage(content="Tu es un assistant utile et concis."),
    HumanMessage(content="Explique-moi ce qu'est un LLM en 3 phrases."),
]

response = model.invoke(prompt)
print(response.content)
