#!/usr/bin/env python3

# https://docs.langchain.com/oss/python/integrations/providers/mistralai
# https://docs.mistral.ai/getting-started/quickstarts/developer/first-api-request

import base64
import getpass
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_mistralai import ChatMistralAI
import os
    

if "MISTRAL_API_KEY" not in os.environ:
    os.environ["MISTRAL_API_KEY"] = getpass.getpass("Enter your Mistral API key: ")


def load_image_as_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Models overview: https://docs.mistral.ai/models/overview
model = ChatMistralAI(
    # model="mistral-large-latest",
    # model="ministral-8b-2512",
    model="mistral-small-2603",
)

image_path = "image.png"
image_data = load_image_as_base64(image_path)

prompt = [
    HumanMessage(
        content=[
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_data}"
                },
            },
            {
                "type": "text",
                "text": "What do you see in this image?"
            },
        ]
    )
]

output = model.invoke(prompt)
print(f"Output: {output.content}")