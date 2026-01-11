#!/usr/bin/env python3

# C.f. https://docs.ray.io/en/latest/ray-overview/getting-started.html#ray-core-quickstart

import ray

ray.init()

@ray.remote
def f(x):
    return x * x

future_res1 = f.remote(1)
future_res2 = f.remote(2)

print(ray.get(future_res1))  # 1
print(ray.get(future_res2))  # 4

input("Press Enter to stop Ray...")