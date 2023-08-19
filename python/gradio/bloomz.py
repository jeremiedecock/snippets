#!/usr/bin/env python3

# To run this demo, type in a terminal: gradio bloomz.py

import random
import gradio as gr

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("bigscience/mt0-small")
model = AutoModelForSeq2SeqLM.from_pretrained("bigscience/mt0-small")

def random_response(message, history):
    return random.choice(["Yes", "No"])

demo = gr.ChatInterface(random_response)

demo.launch()
