#!/usr/bin/env python3

import torch

class ExampleDataset(torch.utils.data.Dataset):
    def __init__(self, transform=None, target_transform=None):
        super().__init__()
        self._x = torch.arange(0, 10).float()
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

train_size = int(0.6 * len(dataset))
val_size = len(dataset) - train_size

train_subset, val_subset = torch.utils.data.random_split(dataset, [train_size, val_size])

train_loader = torch.utils.data.DataLoader(train_subset, batch_size=2, shuffle=True)
val_loader = torch.utils.data.DataLoader(val_subset, batch_size=2, shuffle=False)

print("Train set:")

for X, y in train_loader:
    print("X:", X)
    # print("y:", y)
    # print()

print()
print("Validation set:")

for X, y in val_loader:
    print("X:", X)
    # print("y:", y)
    # print()
