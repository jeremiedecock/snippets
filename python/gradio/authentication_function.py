#!/usr/bin/env python3

# To run this demo, type in a terminal: gradio authentication_function.py

# See: https://www.gradio.app/guides/sharing-your-app#authentication

# You can pass a function that takes a username and password as arguments,
# and returns True to allow authentication, False otherwise.
# This can be used for, among other things, making requests to 3rd-party
# authentication services.

import gradio as gr

def greet(name):
    return "Hello " + name + "!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")

def auth_fn(username, password):
    """A bogus authentication function that accepts any login where the username and password are the same."""
    return username == password

demo.launch(auth=auth_fn)
