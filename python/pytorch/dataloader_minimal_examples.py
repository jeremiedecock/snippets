#!/usr/bin/env python3

import torch

class ExampleDataset(torch.utils.data.Dataset):
    def __init__(self):
        super().__init__()
        self._x = torch.arange(0, 6).float()
        self._y = self._x % 2

    def __len__(self):
        return len(self._x)

    def __getitem__(self, idx):
        x = self._x[idx]
        y = self._y[idx]

        return x, y

dataset = ExampleDataset()

dataloader = torch.utils.data.DataLoader(dataset)

for X, y in dataloader:
    print("X:", X)
    print("y:", y)
    print()
