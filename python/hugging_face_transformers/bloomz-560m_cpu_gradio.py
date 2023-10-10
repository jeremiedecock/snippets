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
    outputs = model.generate(inputs, do_sample=True, top_p=0.95, top_k=60, temperature=0.9, max_length=1000, num_return_sequences=1)

    return tokenizer.decode(outputs[0])


examples = [
    "Translate to English: Je t’aime.",
    "Write a fairy tale about a troll saving a princess from a dangerous dragon. The fairy tale is a masterpiece that has achieved praise worldwide and its moral is \"Heroes Come in All Shapes and Sizes\". Story (in French):",
    "Explain in a sentence in French what is backpropagation in neural networks."
]

demo = gr.ChatInterface(chat,
                        examples=examples,
                        title="BloomZ 560M",
                        description="See: https://huggingface.co/bigscience/bloomz-560m")

demo.launch()