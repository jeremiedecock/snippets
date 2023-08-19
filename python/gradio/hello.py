#!/usr/bin/env python3

# To run this demo, type in a terminal: gradio hello.py

import gradio as gr

def greet(name):
    return "Hello " + name + "!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")

demo.launch()
