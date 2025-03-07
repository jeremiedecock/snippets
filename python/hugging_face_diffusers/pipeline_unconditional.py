#!/usr/bin/env python3

# c.f. https://huggingface.co/docs/diffusers/using-diffusers/unconditional_image_generation

from diffusers import DiffusionPipeline

generator = DiffusionPipeline.from_pretrained("anton-l/ddpm-butterflies-128").to("cpu")
image = generator().images[0]
image.save("butterfly.png")
