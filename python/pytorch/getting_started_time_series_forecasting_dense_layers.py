#!/usr/bin/env python3
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
#from sklearn.datasets import load_boston   # Deprecated in favor of California Housing


device = "cpu"    # Alt.: "cuda" or "mps"

# PREPARE THE DATA ############################################################

# Load the Boston Housing data
class TimeSeriesDataset(torch.utils.data.Dataset):
    def __init__(self, time_series, seq_len=4, pred_len=1):
        super().__init__()
        self._x = torch.tensor(time_series, dtype=torch.float32, device=device)
        self.seq_len = seq_len
        self.pred_len = pred_len

    def __len__(self):
        return len(self._x) - self.seq_len - self.pred_len + 1

    def __getitem__(self, index):
        x = self._x[index:index+self.seq_len]
        y = self._x[index+self.seq_len:index+self.seq_len+self.pred_len]
        return x, y


# Create a time series dataset (very basic example: a sine wave)
training_ts = np.sin(np.linspace(0, 100, 1000) * 2. * np.pi) + np.random.normal(0, 0.1, 1000)
test_ts = np.sin(np.linspace(0, 100, 1000) * 2. * np.pi) + np.random.normal(0, 0.01, 1000)
# plt.plot(training_ts[:8])
# plt.show()

# TODO: For actual time series data, you should normalize the data

SEQ_LEN = 8
PRED_LEN = 2

training_data = TimeSeriesDataset(time_series=training_ts, seq_len=SEQ_LEN, pred_len=PRED_LEN)
test_data = TimeSeriesDataset(time_series=test_ts, seq_len=SEQ_LEN, pred_len=PRED_LEN)

input_dim = training_data[0][0].shape[0]   # SEQ_LEN
output_dim = training_data[0][1].shape[0]  # PRED_LEN


# INSTANTIATE DATALOADERS #####################################################

batch_size = 32

train_dataloader = DataLoader(training_data, batch_size=batch_size, shuffle=True)
test_dataloader = DataLoader(test_data, batch_size=batch_size, shuffle=True)      # TODO


# CREATING MODELS #############################################################

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()

        self.linear_relu_stack = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, output_dim)
        )

    def forward(self, x):
        return self.linear_relu_stack(x)

model = NeuralNetwork().to(device)

print(model)



# OPTIMIZE THE MODEL PARAMETERS ###############################################

loss_fn = nn.MSELoss()
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

mae_fn = nn.L1Loss()

def test(dataloader, model, loss_fn):
    dataset_size = len(dataloader.dataset)
    num_batches = len(dataloader)
    test_mse = 0  # Loss
    test_mae = 0  # Metrics

    model.eval()

    with torch.no_grad():
        for X, y_true in dataloader:
            X, y_true = X.to(device), y_true.to(device)
            y_pred = model(X)
            test_mse += loss_fn(y_pred, y_true).item()
            test_mae += mae_fn(y_pred, y_true).item()

    test_mse /= num_batches
    test_mae /= num_batches

    print(f"Test Error: \n Avg MAE: {test_mae:>8f}, Avg MSE: {test_mse:>8f} \n")


# TRAIN THE MODEL #############################################################

epochs = 5
for epoch in range(epochs):
    print(f"Epoch {epoch+1}/{epochs}\n-------------------------------")

    train(train_dataloader, model, loss_fn, optimizer)
    test(test_dataloader, model, loss_fn)


# SAVE THE MODEL ##############################################################

torch.save(model, "getting_started_time_series_forecasting_dense_layers.pth")


# MAKE PREDICTIONS WITH THE TRAINED ###########################################

model.eval()

x = test_data[0][0].unsqueeze(0)  # Add batch dimension
y_true = test_data[0][1]

with torch.no_grad():
    x = x.to(device)
    y_pred = model(x)
    print(f'Predicted: "{y_pred}", Actual: "{y_true}"')