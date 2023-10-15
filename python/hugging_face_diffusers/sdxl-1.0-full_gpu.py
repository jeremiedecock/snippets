#!/usr/bin/env python3

# c.f. https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0

from diffusers import DiffusionPipeline
import datetime
import torch

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

# prompt = "An astronaut riding a green horse"
prompt = "A majestic lion jumping from a big stone at night"
prompt = "Paris dans les années 1900"

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

image.save(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png")
