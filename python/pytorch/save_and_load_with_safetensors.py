#!/usr/bin/env python3

import torch
import safetensors.torch

# Install safetensors with pip (requires Numpy): pip install numpy safetensors

# Documentation: https://huggingface.co/docs/safetensors/torch_shared_tensors


# CREATE A BASIC MODEL ########################################################

model = torch.nn.Linear(2, 1)

print("Initial model:", model.state_dict())


# SAVE THE MODEL ##############################################################

safetensors.torch.save_model(model, "model.safetensors")


# RESET THE MODEL #############################################################

# Put the model's parameters to zero
for param in model.parameters():
    param.data.zero_()

print("Reset the model:", model.state_dict())


# LOAD THE MODEL ##############################################################

safetensors.torch.load_model(model, "model.safetensors")

print("Loaded model:", model.state_dict())