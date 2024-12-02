#!/usr/bin/env python3

import torch

class TimeSeriesDataset(torch.utils.data.Dataset):
    def __init__(self, seq_len=4, pred_len=1):
        super().__init__()
        self._x = torch.arange(0, 24).float()
        self.seq_len = seq_len
        self.pred_len = pred_len

    def __len__(self):
        return len(self._x) - self.seq_len - self.pred_len + 1

    def __getitem__(self, index):
        x = self._x[index:index+self.seq_len]
        y = self._x[index+self.seq_len:index+self.seq_len+self.pred_len]
        return x, y

dataset = TimeSeriesDataset(seq_len=4, pred_len=1)

dataloader = torch.utils.data.DataLoader(dataset, batch_size=1, shuffle=False)

for X, y in dataloader:
    print("X:", X)
    print("y:", y)
    print()