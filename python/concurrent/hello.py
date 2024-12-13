#!/usr/bin/env python3

from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
import os
import time

NUM_CPU_CORES = cpu_count()


def run_task(input_param: float):
    print(f"Running task with input param {input_param} on process {os.getpid()}")
    time.sleep(5)
    result = input_param * 2.
    return result


def run_tasks() -> None:
    input_params = [float(x) for x in range(32)]

    with ProcessPoolExecutor(max_workers=NUM_CPU_CORES - 1) as executor:
        futures = [executor.submit(run_task, input_param) for input_param in input_params]

        for future in as_completed(futures):
            result = future.result()  # Ensure any exceptions are raised
            print(f"Result: {result}")


if __name__ == '__main__':
    run_tasks()