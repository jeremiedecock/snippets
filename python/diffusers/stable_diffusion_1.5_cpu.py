# c.f. https://huggingface.co/docs/diffusers/quicktour#diffusionpipeline

from diffusers import DiffusionPipeline

pipeline = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
#pipeline.to("cuda")   # requires a GPU with > 6Go VRAM

image = pipeline("An image of a squirrel in Picasso style").images[0]
image.save("squirrel_1.5.png")
