#!/usr/bin/env python3

# Source: https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0

# To run this demo, type in a terminal: gradio sdxl-1.0-base_gpu_gradio.py

# Model "stable-diffusion-xl-base-1.0"

from diffusers import DiffusionPipeline
import torch

import gradio as gr

pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
pipe.to("cuda")

# if using torch < 2.0
# pipe.enable_xformers_memory_efficient_attention()

def generate_image(prompt):
    image = pipe(prompt=prompt).images[0]

    return image


demo = gr.Interface(generate_image, "text", "image")

demo.launch()