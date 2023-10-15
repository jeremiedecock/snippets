#!/usr/bin/env python3

# Source: https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0

# To run this demo, type in a terminal: gradio sdxl-1.0-base_gpu_gradio.py

# Model "stable-diffusion-xl-base-1.0"

from diffusers import DiffusionPipeline
import torch

import gradio as gr

# load both base & refiner
base = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0",
                                         torch_dtype=torch.float16,
                                         variant="fp16",
                                         use_safetensors=True)
base.to("cuda")

refiner = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-refiner-1.0",
                                            text_encoder_2=base.text_encoder_2,
                                            vae=base.vae,
                                            torch_dtype=torch.float16,
                                            use_safetensors=True,
                                            variant="fp16")
refiner.to("cuda")

# Define how many steps and what % of steps to be run on each experts (80/20) here
n_steps = 40
high_noise_frac = 0.8

# if using torch < 2.0
# pipe.enable_xformers_memory_efficient_attention()

def generate_image(prompt):
    # run both experts
    image = base(
        prompt=prompt,
        num_inference_steps=n_steps,
        denoising_end=high_noise_frac,
        output_type="latent",
    ).images

    image = refiner(
        prompt=prompt,
        num_inference_steps=n_steps,
        denoising_start=high_noise_frac,
        image=image,
    ).images[0]

    return image


demo = gr.Interface(generate_image, "text", "image")

demo.launch(server_name="0.0.0.0")