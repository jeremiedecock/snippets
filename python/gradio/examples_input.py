#!/usr/bin/env python3

# See: https://www.gradio.app/guides/key-features#example-inputs

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import gradio as gr

checkpoint = "bigscience/mt0-small"

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

def chat(message, history):
    # TODO: use `history`
    inputs = tokenizer.encode(message, return_tensors="pt")
    outputs = model.generate(inputs)

    return tokenizer.decode(outputs[0])


examples = [
    "Translate to English: Je t’aime.",
    "Write a fairy tale about a troll saving a princess from a dangerous dragon. The fairy tale is a masterpiece that has achieved praise worldwide and its moral is \"Heroes Come in All Shapes and Sizes\". Story (in French):",
    "Explain in a sentence in French what is backpropagation in neural networks."
]

demo = gr.ChatInterface(chat,
                        examples=examples,
                        title="mT0-small",
                        description="See: https://huggingface.co/bigscience/mt0-small")

demo.launch()