#!/usr/bin/env python3

import torch


# CREATE A BASIC MODEL ########################################################

model = torch.nn.Linear(2, 1)

print("Initial model:", model.state_dict())


# SAVE THE MODEL ##############################################################

torch.save(model, "model.pt")


# RESET THE MODEL #############################################################

# Put the model's parameters to zero
for param in model.parameters():
    param.data.zero_()

print("Reset the model:", model.state_dict())


# LOAD THE MODEL ##############################################################

model = torch.load("model.pt", weights_only=False)

print("Loaded model:", model.state_dict())