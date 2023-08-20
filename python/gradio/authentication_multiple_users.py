#!/usr/bin/env python3

# To run this demo, type in a terminal: gradio authentication_multiple_users.py

# See: https://www.gradio.app/guides/sharing-your-app#authentication

import gradio as gr

def greet(name):
    return "Hello " + name + "!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")

demo.launch(auth=[("john", "pass1234"), ("alice", "pass5678"), ("bob", "pass9012")])
