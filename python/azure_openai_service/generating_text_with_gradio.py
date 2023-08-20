#!/usr/bin/env python3

# See: https://learn.microsoft.com/en-us/azure/cognitive-services/openai/quickstart?pivots=programming-language-python&tabs=command-line

# To run this demo, type in a terminal: gradio generating_text_with_gradio.py

import openai
import gradio as gr

from credentials import AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT_NAME

openai.api_key = AZURE_OPENAI_API_KEY
openai.api_base = AZURE_OPENAI_ENDPOINT     # Your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
openai.api_type = 'azure'
openai.api_version = '2023-05-15'           # This may change in the future


def chat(start_phrase, history):
    # TODO: use `history`
    response = openai.Completion.create(engine=AZURE_OPENAI_DEPLOYMENT_NAME, prompt=start_phrase, max_tokens=10)

    return response['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()


demo = gr.ChatInterface(chat)

demo.launch()