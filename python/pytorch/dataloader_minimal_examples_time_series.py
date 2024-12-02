#!/usr/bin/env python3

# Ref: https://stackoverflow.com/a/63977886

import torch

class ExampleDataset(torch.utils.data.Dataset):
    def __init__(self, seq_len=4):
        super().__init__()
        self._x = torch.arange(0, 24).float()
        self._y = self._x % 2
        self.seq_len = seq_len

    def __len__(self):
        return self._x.__len__() - (self.seq_len - 1)

    def __getitem__(self, index):
        x = self._x[index:index+self.seq_len]
        y = self._y[index:index+self.seq_len]
        return x, y

dataset = ExampleDataset()

dataloader = torch.utils.data.DataLoader(dataset)

for X, y in dataloader:
    print("X:", X)
    print("y:", y)
    print()
