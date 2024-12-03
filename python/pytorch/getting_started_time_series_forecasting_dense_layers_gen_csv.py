#!/usr/bin/env python3
# coding: utf-8

import argparse
from clearml import Task
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import torch
from torch import nn
from torch.utils.data import DataLoader


def main():
    """Main function"""

    parser = argparse.ArgumentParser(description='Generate a dataset in a CSV.')

    parser.add_argument("--output", "-o", default="getting_started_time_series_forecasting_dense_layers_args.csv", metavar="STRING",
        help="the path of the CSV file that contains the time series")

    parser.add_argument("--plot", "-p", action="store_true",
        help="plot the time series")

    args = parser.parse_args()


    # GENERATE THE DATA #######################################################

    # Create a time series dataset (very basic example: a sine wave)
    training_ts = np.sin(np.linspace(0, 100, 1000) * 2. * np.pi) + np.random.normal(0, 0.1, 1000)
    test_ts = np.sin(np.linspace(0, 100, 1000) * 2. * np.pi) + np.random.normal(0, 0.1, 1000)

    df = pd.DataFrame({"training": training_ts, "test": test_ts})
    df.to_csv(args.output, index=False)

    if args.plot:
        df.plot()
        plt.show()


if __name__ == '__main__':
    main()