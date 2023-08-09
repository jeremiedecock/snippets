#!/usr/bin/env python3

import torch

model = torch.nn.Sequential( torch.nn.Linear(2, 1, bias=False) )

x = torch.tensor([0., 1.])
y = model(x)

print(x, y)

print(model.state_dict())
