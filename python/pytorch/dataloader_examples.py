#!/usr/bin/env python3

import torch

class ExampleDataset(torch.utils.data.Dataset):
    def __init__(self, transform=None, target_transform=None):
        super().__init__()
        self._x = torch.arange(0, 6).float()
        self._y = self._x % 2

        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self._x)

    def __getitem__(self, idx):
        x = self._x[idx]
        y = self._y[idx]

        if self.transform:
            x = self.transform(x)
        if self.target_transform:
            y = self.target_transform(y)

        return x, y

dataset = ExampleDataset()

dataloader = torch.utils.data.DataLoader(dataset, batch_size=2, shuffle=True)

for X, y in dataloader:
    print("X:", X)
    print("y:", y)
    print()
