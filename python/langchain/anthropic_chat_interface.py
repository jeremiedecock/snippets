#!/usr/bin/env python3

# https://docs.langchain.com/oss/python/integrations/providers/anthropic
# https://platform.claude.com/
# https://claude.com/platform/api

import getpass
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
import os

if "ANTHROPIC_API_KEY" not in os.environ:
    os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter your Anthropic API key: ")

model = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    # temperature=,
    # max_tokens=,
    # timeout=,
    # max_retries=,
    # ...
)

prompt = [
    SystemMessage(content="Tu es un assistant utile et concis."),
    HumanMessage(content="Explique-moi ce qu'est un LLM en 3 phrases."),
]

response = model.invoke(prompt)
print(response.content)
