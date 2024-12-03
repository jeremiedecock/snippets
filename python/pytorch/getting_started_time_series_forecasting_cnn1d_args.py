#!/usr/bin/env python3
# coding: utf-8

# Usage example:
# ./getting_started_time_series_forecasting_cnn1d_args.py --train-csv=getting_started_time_series_forecasting_dense_layers_args.csv --test-csv=getting_started_time_series_forecasting_dense_layers_args.csv --train-column=0 --test-column=1 --train-skip=1 --test-skip=1 --seq-len=48 --pred-len=24 --plot

import argparse
from clearml import Task
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
import torch
from torch import Tensor
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from typing import Optional, Tuple

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# PREPARE THE DATA ############################################################

class TimeSeriesDataset(torch.utils.data.Dataset):
    def __init__(
        self,
        time_series: Tensor,
        seq_len:int,
        pred_len:int,
        device: str =DEVICE
    ) -> None:
        super().__init__()
        self._x = torch.tensor(time_series, dtype=torch.float32, device=device)
        self.seq_len = seq_len
        self.pred_len = pred_len

    def __len__(self) -> int:
        return len(self._x) - self.seq_len - self.pred_len + 1

    def __getitem__(self, index: int) -> Tuple[Tensor, Tensor]:
        x = self._x[index:index+self.seq_len]
        y = self._x[index+self.seq_len:index+self.seq_len+self.pred_len]
        return x, y


# CREATING MODELS #############################################################

class TimeSeriesModel(torch.nn.Module):
    def __init__(self, input_dim: int, output_dim: int) -> None:
        super(TimeSeriesModel, self).__init__()
        self.conv1 = torch.nn.Conv1d(in_channels=1, out_channels=64, kernel_size=3, padding=1)
        self.conv2 = torch.nn.Conv1d(in_channels=64, out_channels=64, kernel_size=3, padding=1)
        self.fc = torch.nn.Linear(input_dim * 64, output_dim)

    def forward(self, x: Tensor) -> Tensor:
        x = x.unsqueeze(1)  # Add channel dimension
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = x.view(x.size(0), -1)  # Flatten
        x = self.fc(x)
        return x


# DEFINE THE TRAINING LOOP ####################################################

def train(
    dataloader: DataLoader,
    model: torch.nn.Module,
    loss_fn: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    epoch: int,
    device: str = DEVICE,
    writer: Optional[SummaryWriter] = None
) -> None:
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
            if writer is not None:
                writer.add_scalar('MSE/train', train_loss, epoch)


# DEFINE THE TESTING LOOP #####################################################

def test(
    dataloader: DataLoader,
    model: torch.nn.Module,
    loss_fn: torch.nn.Module,
    metrics_fn: torch.nn.Module,
    epoch: int,
    device: str = DEVICE,
    writer: Optional[SummaryWriter] = None
) -> None:
    model.eval()

    num_samples = len(dataloader.dataset)

    test_mse = 0  # Loss
    test_mae = 0  # Metrics

    with torch.no_grad():
        for X, y_true in dataloader:
            X, y_true = X.to(device), y_true.to(device)
            y_pred = model(X)
            test_mse += loss_fn(y_pred, y_true).item()
            test_mae += metrics_fn(y_pred, y_true).item()

    test_mse /= num_samples   # Average loss over all samples
    test_mae /= num_samples   # Average metrics over all samples

    print(f"Test Error: \n Avg MAE: {test_mae:>8f}, Avg MSE: {test_mse:>8f} \n")

    # Log the loss values to TensorBoard
    if writer is not None:
        writer.add_scalar('MSE/test', test_mse, epoch)
        writer.add_scalar('MAE', test_mae, epoch)


# MAKE PREDICTIONS WITH THE TRAINED ###########################################

def plot_test(
    x: Tensor,
    y_true: Tensor,
    y_pred: Tensor,
    seq_len: int,
    pred_len: int
) -> None:
    # Plot the sequence (blue plain line), the prediction (red dotted line) and the actual values (blue dotted line)
    plt.plot(x.cpu().numpy().flatten(), label='Sequence', color='b')
    plt.plot(range(seq_len, seq_len+pred_len), y_pred.cpu().numpy().flatten(), '--', label='Prediction', color='r')
    plt.plot(range(seq_len, seq_len+pred_len), y_true.cpu().numpy().flatten(), '--', label='Actual', color='b')
    plt.legend()
    plt.show()



# MAIN FUNCTION ###############################################################

def main() -> None:
    """Main function"""

    parser = argparse.ArgumentParser(description='Forecast a time series.')

    parser.add_argument("--train-csv", "-t", default="getting_started_time_series_forecasting_dense_layers_args.csv", metavar="STRING",
        help="the CSV file that contains the training time series")

    parser.add_argument("--train-column", "-i", type=int, default=0, metavar="INTEGER",
        help="the column index of the training time series in the CSV file (default: 0)")

    parser.add_argument("--train-skip", "-r", type=int, default=0, metavar="INTEGER",
        help="the number of rows to skip in the train CSV file (default: 0)")

    parser.add_argument("--test-csv", "-T", default="getting_started_time_series_forecasting_dense_layers_args.csv", metavar="STRING",
        help="the CSV file that contains the test time series")

    parser.add_argument("--test-column", "-I", type=int, default=1, metavar="INTEGER",
        help="the column index of the test time series in the CSV file (default: 0)")

    parser.add_argument("--test-skip", "-R", type=int, default=0, metavar="INTEGER",
        help="the number of rows to skip in the test CSV file (default: 0)")

    parser.add_argument("--seq-len", "-s", type=int, default=32, metavar="INTEGER",
        help="the sequence length used to predict the next values (default: 32)")

    parser.add_argument("--pred-len", "-S", type=int, default=16, metavar="INTEGER",
        help="the length of the prediction sequence (default: 16)")

    parser.add_argument("--device", "-d", default=DEVICE, metavar="STRING",
        help=f"the CSV file that contains the training time series (default: {DEVICE})")

    parser.add_argument("--epochs", "-e", type=int, default=5, metavar="INTEGER",
        help="the number of epochs (default: 5)")

    parser.add_argument("--batch-size", "-b", type=int, default=32, metavar="INTEGER",
        help="the batch size (default: 32)")

    parser.add_argument("--learning_rate", "-l", type=float, default=0.001, metavar="FLOAT",
        help="the learning rate (default: 0.001)")

    parser.add_argument("--plot", "-p", action="store_true",
        help="plot the time series")

    parser.add_argument("--randomize",  "-x", action="store_true",
        help="don't use a fixed seed (for reproducibility)")

    args = parser.parse_args()


    # SETTING THE RANDOM SEED #################################################

    # See https://clear.ml/docs/latest/docs/clearml_sdk/task_sdk/#setting-random-seed
    if not args.randomize:
        Task.set_random_seed(None)


    # INITIALIZING CLEARML TASK ###############################################

    task = Task.init(project_name="Snippets", task_name="Timeseries forecasting with CNN 1D")


    # INITIALIZING TENSORBOARD SUMMARYWRITER ##################################

    writer = SummaryWriter()

    print("Starting training...\nTo visualize the data from a local machine, run the following command in the terminal:\n\ntensorboard --logdir=runs\n\nthen open a web browser and go at the address mentioned in the terminal (usually http://localhost:6006/).")


    # GENERATE THE DATA #######################################################

    training_ts = pd.read_csv(args.train_csv, usecols=[args.train_column], skiprows=args.train_skip).values.flatten()
    test_ts = pd.read_csv(args.test_csv, usecols=[args.test_column], skiprows=args.test_skip).values.flatten()

    if args.plot:
        plt.plot(training_ts, label='Training')
        plt.plot(test_ts, label='Test')
        plt.show()

    # TODO: For actual time series data, you should normalize the data

    training_data = TimeSeriesDataset(time_series=training_ts, seq_len=args.seq_len, pred_len=args.pred_len)
    test_data = TimeSeriesDataset(time_series=test_ts, seq_len=args.seq_len, pred_len=args.pred_len)


    # INSTANTIATE DATALOADERS #####################################################

    train_dataloader = DataLoader(training_data, batch_size=args.batch_size, shuffle=True)
    test_dataloader = DataLoader(test_data, batch_size=args.batch_size, shuffle=True)


    # INSTANTIATE THE MODEL ###################################################

    model = TimeSeriesModel(input_dim=args.seq_len, output_dim=args.pred_len).to(args.device)

    print(model)


    # OPTIMIZE THE MODEL PARAMETERS ###########################################

    loss_fn = torch.nn.MSELoss()
    metrics_fn = torch.nn.L1Loss()

    optimizer = torch.optim.Adam(model.parameters(), lr=args.learning_rate)


    # TRAIN THE MODEL #########################################################

    for epoch in range(args.epochs):
        print(f"Epoch {epoch+1}/{args.epochs}\n-------------------------------")

        train(
            dataloader=train_dataloader,
            model=model,
            loss_fn=loss_fn,
            optimizer=optimizer,
            epoch=epoch,
            device=args.device,
            writer=writer
        )

        test(
            dataloader=test_dataloader,
            model=model,
            loss_fn=loss_fn,
            metrics_fn=metrics_fn,
            epoch=epoch,
            device=args.device,
            writer=writer
        )


    # CLOSING SUMMARYWRITER ###################################################

    writer.close()


    # SAVE THE MODEL ##########################################################

    torch.save(model, "getting_started_time_series_forecasting_cnn1d.pth")


    # MAKE PREDICTIONS WITH THE TRAINED #######################################

    model.eval()

    test_dataloader = DataLoader(test_data, batch_size=1, shuffle=True)

    for sample_index, (x, y_true) in enumerate(test_dataloader):
        with torch.no_grad():
            x = x.to(args.device)
            y_pred = model(x)
            print(f'Predicted: "{y_pred}", Actual: "{y_true}"')

            if args.plot:
                plot_test(x, y_true, y_pred, args.seq_len, args.pred_len)

        if sample_index >= 3:
            break


if __name__ == '__main__':
    main()