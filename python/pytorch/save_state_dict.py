#!/usr/bin/env python3

import torch


# CREATE A BASIC MODEL ########################################################

model = torch.nn.Linear(2, 1)

print("Initial model:", model.state_dict())


# SAVE THE MODEL ##############################################################

torch.save(model.state_dict(), "model.pt")


# RESET THE MODEL #############################################################

# Put the model's parameters to zero
for param in model.parameters():
    param.data.zero_()

print("Reset the model:", model.state_dict())


# LOAD THE MODEL ##############################################################

model.load_state_dict(torch.load("model.pt"))

print("Loaded model:", model.state_dict())