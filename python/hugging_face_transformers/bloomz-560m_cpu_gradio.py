#!/usr/bin/env python3

# Source: https://huggingface.co/bigscience/bloomz-560m#cpu

# To run this demo, type in a terminal: gradio bloomz-560m_cpu_gradio.py

# Model "bigscience/bloomz-560m" (560M parameters): multitask finetuned on xP3.
# Recommended for prompting in English. 
# See: https://huggingface.co/bigscience/bloomz-560m

from transformers import AutoTokenizer, AutoModelForCausalLM
import gradio as gr

checkpoint = "bigscience/bloomz-560m"

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint)

def chat(message, history):
    # TODO: use `history`
    inputs = tokenizer.encode(message, return_tensors="pt")
    outputs = model.generate(inputs)

    return tokenizer.decode(outputs[0])


demo = gr.ChatInterface(chat)

demo.launch()