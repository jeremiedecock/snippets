#!/usr/bin/env python3
# coding: utf-8

# Source: https://pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html#

import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor


# DOWNLOAD THE MNIST DATASET ##################################################

training_data = datasets.MNIST(root="data", train=True, download=True, transform=ToTensor())
test_data = datasets.MNIST(root="data", train=False, download=True, transform=ToTensor())


# INSTANTIATE DATALOADERS #####################################################

batch_size = 64

train_dataloader = DataLoader(training_data, batch_size=batch_size)
test_dataloader = DataLoader(test_data, batch_size=batch_size)


# CREATING MODELS #############################################################

device = "cpu"    # Alt.: "cuda" or "mps"

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()

        self.flatten = nn.Flatten()

        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28*28, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 10)
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

model = NeuralNetwork().to(device)

print(model)


# OPTIMIZE THE MODEL PARAMETERS ###############################################

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters())


# DEFINE THE TRAINING LOOP ####################################################

def train(dataloader, model, loss_fn, optimizer):
    dataset_size = len(dataloader.dataset)

    model.train()

    for batch_idx, (X, y_true) in enumerate(dataloader):
        X, y_true = X.to(device), y_true.to(device)

        # Compute prediction error
        y_pred = model(X)
        train_loss = loss_fn(y_pred, y_true)

        # Backpropagation
        train_loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        # Print status
        if batch_idx % 100 == 0:
            train_loss = train_loss.item()
            train_step = (batch_idx + 1) * len(X)

            print(f"loss: {train_loss:>7f}  [{train_step:>5d}/{dataset_size:>5d}]")



# DEFINE THE TESTING LOOP #####################################################

def test(dataloader, model, loss_fn):
    dataset_size = len(dataloader.dataset)
    num_batches = len(dataloader)
    test_loss = 0
    correct = 0

    model.eval()

    with torch.no_grad():
        for X, y_true in dataloader:
            X, y_true = X.to(device), y_true.to(device)
            y_pred = model(X)
            test_loss += loss_fn(y_pred, y_true).item()
            correct += (y_pred.argmax(1) == y_true).type(torch.float).sum().item()

    test_loss /= num_batches
    test_accuracy = 100. * correct / dataset_size

    print(f"Test Error: \n Accuracy: {test_accuracy:>0.1f}%, Avg loss: {test_loss:>8f} \n")


# TRAIN THE MODEL #############################################################

epochs = 5
for epoch in range(epochs):
    print(f"Epoch {epoch+1}/{epochs}\n-------------------------------")

    train(train_dataloader, model, loss_fn, optimizer)
    test(test_dataloader, model, loss_fn)


# SAVE THE MODEL ##############################################################

torch.save(model, "mnist_model.pth")


# MAKE PREDICTIONS WITH THE TRAINED ###########################################

model.eval()

x = test_data[0][0]
y_true = test_data[0][1]

with torch.no_grad():
    x = x.to(device)
    y_pred = model(x)
    print(f'Predicted: "{y_pred[0].argmax(0)}", Actual: "{y_true}"')
