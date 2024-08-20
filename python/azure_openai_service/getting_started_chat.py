#!/usr/bin/env python3

# See: https://learn.microsoft.com/en-us/azure/cognitive-services/openai/quickstart?pivots=programming-language-python&tabs=command-line

from openai import AzureOpenAI

from credentials import AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT_NAME

client = AzureOpenAI(
    azure_endpoint = AZURE_OPENAI_ENDPOINT,   # Your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
    api_key=AZURE_OPENAI_API_KEY,  
    api_version="2023-05-15" # model_dict["api_version"]
)

# A chat test

PROMPT_STR = "Explain in a sentence in French what is backpropagation in neural networks."

print(PROMPT_STR)

messages = [
    {
        "role": "system",
        "content": "You are an AI assistant that helps people find information."
    },
    {
        "role": "user",
        "content": PROMPT_STR
    }
]

try:
    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT_NAME,
        messages = messages,
        # temperature=0.7,
        # max_tokens=800,
        # top_p=0.95,
        # frequency_penalty=0,
        # presence_penalty=0,
        # #stream=True,          # see https://www.gradio.app/guides/creating-a-chatbot-fast#a-streaming-example-using-openai
        # stop=None
    )

    assistant_msg = response.choices[0].message.content
    status = "success"
except Exception as e:
    print(f"chat error {e}")

print("Answer:\n" + assistant_msg)
