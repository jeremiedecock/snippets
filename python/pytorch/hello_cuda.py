#!/usr/bin/env python3

import torch

print("Number of CUDA devices:", torch.cuda.device_count())

for device_index in range(torch.cuda.device_count()):
    print(torch.cuda.get_device_name(device_index))
