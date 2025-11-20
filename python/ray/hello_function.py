#!/usr/bin/env python3

# C.f. https://docs.ray.io/en/latest/ray-overview/getting-started.html#ray-core-quickstart

import ray

ray.init()

@ray.remote
def f(x):
    return x * x

futures = [f.remote(i) for i in range(4)]
results = ray.get(futures)

print(results) # [0, 1, 4, 9]