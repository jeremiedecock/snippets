#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import torch


# PREPARE THE DATA ############################################################

class TimeSeriesDataset(torch.utils.data.Dataset):
    def __init__(
        self,
        wave1_freq: float = .1,
        wave1_amp: float = 1.0,
        wave1_phase: float = 0.0,
        wave2_freq: float = 0.01,
        wave2_amp: float = 1.0,
        wave2_phase: float = 0.0,
        trend_slope: float = 0., # 0.01,
        trend_intercept: float = 0.0,
        noise_scale: float = 0., # 0.5
        total_length: int = 1024,
        history_length: int = 32,
        prediction_horizon: int = 16,
        device: str = "cpu",
    ):
        super().__init__()

        # First wave component
        self.wave1_freq = wave1_freq
        self.wave1_amp = wave1_amp
        self.wave1_phase = wave1_phase

        # Second wave component
        self.wave2_freq = wave2_freq
        self.wave2_amp = wave2_amp
        self.wave2_phase = wave2_phase

        # Trend and noise parameters
        self.trend_slope = trend_slope
        self.trend_intercept = trend_intercept
        self.noise_scale = noise_scale

        # Sequence parameters
        self.total_length = total_length
        self.history_length = history_length
        self.prediction_horizon = prediction_horizon

        # Technical parameters
        self.device = device

        # Generate the time series data ###################

        # Generate time points
        t = np.arange(self.total_length)

        # Generate components
        wave1 = self.wave1_amp * np.sin(2. * np.pi * self.wave1_freq * t + self.wave1_phase)
        wave2 = self.wave2_amp * np.sin(2. * np.pi * self.wave2_freq * t + self.wave2_phase)
        trend = self.trend_slope * t + self.trend_intercept
        noise = np.random.normal(scale=self.noise_scale, size=self.total_length)

        # Combine components
        series = wave1 + wave2 + trend + noise

        # Convert to tensor
        self.data =  torch.tensor(series, dtype=torch.float32).to(self.device)

    def __len__(self):
        # Number of possible sequences (aka "examples" or "samples"), considering we need both history and prediction windows
        return self.total_length - self.history_length - self.prediction_horizon + 1

    def __getitem__(self, index):
        # TODO: this dataset can bias the model training as parts of the test set are used in the training set...

        # Extract history window
        history_start = index
        history_end = index + self.history_length
        history = self.data[history_start:history_end]

        # Extract future window
        future_start = history_end
        future_end = future_start + self.prediction_horizon
        future = self.data[future_start:future_end]

        return history, future
    
    # def __len__(self):
    #     # Number of non-overlapping sequences
    #     return self.total_length // (self.history_length + self.prediction_horizon)

    # def __getitem__(self, index):
    #     # Calculate starting point for this sequence
    #     start_idx = index * (self.history_length + self.prediction_horizon)
        
    #     # Extract non-overlapping windows
    #     history = self.data[start_idx:start_idx + self.history_length]
    #     future = self.data[start_idx + self.history_length:start_idx + self.history_length + self.prediction_horizon]
        
    #     return history, future

    def plot_full_dataset(self):
        plt.figure(figsize=(10, 4))
        plt.plot(self.data.cpu().numpy(), label='Generated Time Series')
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title('Generated Time Series')
        plt.legend()
        plt.show()


# INSTANTIATE DATASETS ########################################################

dataset = TimeSeriesDataset()
dataset.plot_full_dataset()
