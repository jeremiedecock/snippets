#!/usr/bin/env python3
# coding: utf-8

# Source: lab1_deep_value-based_reinforcement_learning_answers.ipynb in github.com:jeremiedecock/polytechnique-inf639-2024-teachers.git

from clearml import Task
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter

# Initializing ClearML Task
task = Task.init(project_name="Snippets", task_name="PyTorch and Tensorboard on toy example")

# Simple example: model and data
class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc = nn.Linear(10, 1)

    def forward(self, x):
        return self.fc(x)

# Creating a model, optimizer, and loss function
model = SimpleModel()
optimizer = optim.SGD(model.parameters(), lr=0.01)
loss_fn = nn.MSELoss()

# Initializing TensorBoard SummaryWriter
writer = SummaryWriter()

print("Starting training...\nTo visualize the data from a local machine, run the following command in the terminal:\n\ntensorboard --logdir=runs\n\nthen open a web browser and go at the address mentioned in the terminal (usually http://localhost:6006/).")

# Training example
for epoch in range(100):
    # Fake data
    inputs = torch.randn(32, 10)
    targets = torch.randn(32, 1)

    # Forward pass
    outputs = model(inputs)
    loss = loss_fn(outputs, targets)

    # Backpropagation
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # Log the loss values to TensorBoard
    writer.add_scalar('Loss/train', loss.item(), epoch)

# Closing SummaryWriter
writer.close()