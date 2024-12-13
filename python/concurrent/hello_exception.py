#!/usr/bin/env python3

from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
import os
import time
import traceback

NUM_CPU_CORES = cpu_count()


def run_task(input_param: float):
    print(f"Running task with input param {input_param} on process {os.getpid()}")
    time.sleep(5)
    raise Exception("This is an exception")


def run_tasks() -> None:
    input_params = [float(x) for x in range(32)]

    with ProcessPoolExecutor(max_workers=NUM_CPU_CORES - 1) as executor:
        futures = [executor.submit(run_task, input_param) for input_param in input_params]

        for future in as_completed(futures):
            try:
                future.result()  # Ensure any exceptions are raised
            except Exception as e:
                print(f"Exception caught: {e}")
                traceback.print_exc()  # Print the full stack trace
                # executor.shutdown(wait=False)
                break


if __name__ == '__main__':
    run_tasks()