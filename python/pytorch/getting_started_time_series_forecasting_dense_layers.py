#!/usr/bin/env python3
# coding: utf-8

from clearml import Task
import numpy as np
import matplotlib.pyplot as plt
import torch
from torch import nn
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter


device = "cpu"    # Alt.: "cuda" or "mps"


# INITIALIZING CLEARML TASK ###################################################

task = Task.init(project_name="Snippets", task_name="Timeseries forecasting with Dense Layers on a toy problem")


# INITIALIZING TENSORBOARD SUMMARYWRITER ######################################

writer = SummaryWriter()

print("Starting training...\nTo visualize the data from a local machine, run the following command in the terminal:\n\ntensorboard --logdir=runs\n\nthen open a web browser and go at the address mentioned in the terminal (usually http://localhost:6006/).")


# PREPARE THE DATA ############################################################

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
test_ts = np.sin(np.linspace(0, 100, 1000) * 2. * np.pi) + np.random.normal(0, 0.1, 1000)
# plt.plot(training_ts[:8])
# plt.show()

# TODO: For actual time series data, you should normalize the data

SEQ_LEN = 32
PRED_LEN = 16

training_data = TimeSeriesDataset(time_series=training_ts, seq_len=SEQ_LEN, pred_len=PRED_LEN)
test_data = TimeSeriesDataset(time_series=test_ts, seq_len=SEQ_LEN, pred_len=PRED_LEN)

input_dim = training_data[0][0].shape[0]   # SEQ_LEN
output_dim = training_data[0][1].shape[0]  # PRED_LEN


# INSTANTIATE DATALOADERS #####################################################

batch_size = 32

train_dataloader = DataLoader(training_data, batch_size=batch_size, shuffle=True)
test_dataloader = DataLoader(test_data, batch_size=batch_size, shuffle=True)


# CREATING MODELS #############################################################

class TimeSeriesModel(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(TimeSeriesModel, self).__init__()
        self.l1 = nn.Linear(input_dim, 64)
        self.l2 = nn.Linear(64, 64)
        self.l3 = nn.Linear(64, output_dim)

    def forward(self, x):
        x = torch.relu(self.l1(x))
        x = torch.relu(self.l2(x))
        x = self.l3(x)
        return x

model = TimeSeriesModel(input_dim, output_dim).to(device)

print(model)



# OPTIMIZE THE MODEL PARAMETERS ###############################################

loss_fn = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)


# DEFINE THE TRAINING LOOP ####################################################

def train(dataloader, model, loss_fn, optimizer):
    model.train()

    for batch_index, (X, y_true) in enumerate(dataloader):
        X, y_true = X.to(device), y_true.to(device)

        # Compute prediction and loss
        y_pred = model(X)
        train_loss = loss_fn(y_pred, y_true)

        # Backpropagation
        optimizer.zero_grad()
        train_loss.backward()
        optimizer.step()

        # Print status
        if batch_index % 100 == 0:
            train_loss = train_loss.item()
            train_step = (batch_index + 1) * len(X)

            print(f"loss: {train_loss:>7f}  [{train_step:>5d}/{len(dataloader.dataset):>5d}]")

            # Log the loss values to TensorBoard
            writer.add_scalar('MSE/train', train_loss, epoch)


# DEFINE THE TESTING LOOP #####################################################

mae_fn = nn.L1Loss()

def test(dataloader, model, loss_fn):
    model.eval()

    num_samples = len(dataloader.dataset)

    test_mse = 0  # Loss
    test_mae = 0  # Metrics

    with torch.no_grad():
        for X, y_true in dataloader:
            X, y_true = X.to(device), y_true.to(device)
            y_pred = model(X)
            test_mse += loss_fn(y_pred, y_true).item()
            test_mae += mae_fn(y_pred, y_true).item()

    test_mse /= num_samples   # Average loss over all samples
    test_mae /= num_samples   # Average metrics over all samples

    print(f"Test Error: \n Avg MAE: {test_mae:>8f}, Avg MSE: {test_mse:>8f} \n")

    # Log the loss values to TensorBoard
    writer.add_scalar('MSE/test', test_mse, epoch)
    writer.add_scalar('MAE', test_mae, epoch)


# TRAIN THE MODEL #############################################################

epochs = 5
for epoch in range(epochs):
    print(f"Epoch {epoch+1}/{epochs}\n-------------------------------")

    train(train_dataloader, model, loss_fn, optimizer)
    test(test_dataloader, model, loss_fn)

# Closing SummaryWriter
writer.close()


# SAVE THE MODEL ##############################################################

torch.save(model, "getting_started_time_series_forecasting_dense_layers.pth")


# MAKE PREDICTIONS WITH THE TRAINED ###########################################

def plot_test(x, y_true, y_pred):
    # Plot the sequence (blue plain line), the prediction (red dotted line) and the actual values (blue dotted line)
    plt.plot(x.cpu().numpy().flatten(), label='Sequence', color='b')
    plt.plot(range(SEQ_LEN, SEQ_LEN+PRED_LEN), y_pred.cpu().numpy().flatten(), '--', label='Prediction', color='r')
    plt.plot(range(SEQ_LEN, SEQ_LEN+PRED_LEN), y_true.cpu().numpy().flatten(), '--', label='Actual', color='b')
    plt.legend()
    plt.show()

model.eval()

test_dataloader = DataLoader(test_data, batch_size=1, shuffle=True)

for sample_index, (x, y_true) in enumerate(test_dataloader):
    with torch.no_grad():
        x = x.to(device)
        y_pred = model(x)
        print(f'Predicted: "{y_pred}", Actual: "{y_true}"')
        plot_test(x, y_true, y_pred)

    if sample_index >= 3:
        break