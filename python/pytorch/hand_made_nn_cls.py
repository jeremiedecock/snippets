#!/usr/bin/env python3

import torch
from torch import nn

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28*28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10),
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

model = NeuralNetwork()
print(model)

softmax_fn = nn.Softmax(dim=1)

x = torch.rand(1, 28, 28)
logits = model(x)
pred_probas = softmax_fn(logits)
y_pred = pred_probas.argmax(1)

print(y_pred)