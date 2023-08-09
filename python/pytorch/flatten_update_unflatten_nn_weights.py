#!/usr/bin/env python3
import torch

# The following snippet can be useful e.g. for neuroevolution experiments.
# C.f. https://discuss.pytorch.org/t/how-to-flatten-and-then-unflatten-all-model-parameters/34730/8

# Make the model

model = torch.nn.Sequential(torch.nn.Linear(2, 3, bias=False),
                            torch.nn.ReLU(),
                            torch.nn.Linear(3, 2, bias=False),
                            torch.nn.ReLU(),
                            torch.nn.Linear(2, 1, bias=False))

# Print weights

print(model.state_dict())

# Flatten model's weights
# https://pytorch.org/docs/stable/generated/torch.nn.utils.parameters_to_vector.html

param_vec = torch.nn.utils.parameters_to_vector(model.parameters())

# Update weights

param_vec[0] = 0.

# Apply updates to the model
# https://pytorch.org/docs/stable/generated/torch.nn.utils.vector_to_parameters.html

torch.nn.utils.vector_to_parameters(param_vec, model.parameters())

# Print weights (the very first weight now equals 0)

print(model.state_dict())