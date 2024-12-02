#!/usr/bin/env python3
# coding: utf-8

# Source: lab1_deep_value-based_reinforcement_learning_answers.ipynb in github.com:jeremiedecock/polytechnique-inf639-2024-teachers.git

# TensorBoard is a visualization tool developed by Google,
# primarily used to track and visualize metrics during the training of deep learning models.
# While initially designed for TensorFlow, it can also be integrated with **PyTorch**
# through the **torch.utils.tensorboard** API.
# This allows real-time tracking of metrics such as losses, accuracy, computation graphs,
# and even examining images, weight distributions, histograms, and more.
#
# **`SummaryWriter`** is the central tool for logging data to TensorBoard.
# It captures metric values, like loss, for each iteration/epoch.
# 
# This example trains a simple model on fake data (32 samples with 10 features) over 100 epochs,
# and at each epoch, the loss value is sent to TensorBoard via `writer.add_scalar`.
# 
# To visualize the data from a local machine, run the following command in the terminal:
# 
# ```bash
# tensorboard --logdir=runs
# ```
# 
# then open a web browser and go at the address mentioned in the terminal (usually http://localhost:6006/).
# 
# If you are using Google Colab, you can use the **TensorBoard magic** to visualize the data directly in the notebook.
# 
# # Load TensorBoard extension in Colab
# %load_ext tensorboard
# %tensorboard --logdir ./runs
# 
# For mor information, check the Official Documentation:
# - [TensorBoard for PyTorch Documentation](https://pytorch.org/docs/stable/tensorboard.html)
# - [Official TensorBoard Documentation (General)](https://www.tensorflow.org/tensorboard)

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter

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