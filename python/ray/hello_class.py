#!/usr/bin/env python3

# C.f. https://docs.ray.io/en/latest/ray-overview/getting-started.html#ray-core-quickstart

import ray

ray.init() # Only call this once.

@ray.remote
class Counter(object):
    def __init__(self):
        self.n = 0

    def increment(self):
        self.n += 1

    def read(self):
        return self.n

# Instantiate the Counter class
counters = [Counter.remote() for i in range(4)]

# Call the `increment` method
[c.increment.remote() for c in counters]

# Call the `read` method
futures = [c.read.remote() for c in counters]

results = ray.get(futures)

print(results) # [1, 1, 1, 1]