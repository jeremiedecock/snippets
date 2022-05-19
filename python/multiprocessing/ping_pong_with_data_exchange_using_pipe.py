#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

# See https://docs.python.org/3/library/multiprocessing.html
# To exchange objects between processes, use multiprocessing.Queues or
# multiprocessing.Pipes

import multiprocessing
import time
import os

def proc1_func(pipe):
    print("Start proc1")
    
    # Initial data exchange (from proc1 to proc2)
    data_to_send = [1]
    pipe.send(data_to_send)
    print(f"Processus 1 ({os.getpid()}) has sent {data_to_send}")

    for i in range(10):
        received_data = pipe.recv()
        data_to_send = [1]
        pipe.send(data_to_send)
        print(f"Processus 1 ({os.getpid()}) has recieved {received_data} then has sent {data_to_send}")
        time.sleep(.1)

def proc2_func(pipe):
    print("Start proc2")
    for i in range(10):
        received_data = pipe.recv()
        data_to_send = [2]
        pipe.send(data_to_send)
        print(f"Processus 2 ({os.getpid()}) has recieved {received_data} then has sent {data_to_send}")
        time.sleep(.1)

def main():
    """Main function"""

    lock = multiprocessing.Lock()

    # c.f. https://docs.python.org/3/library/multiprocessing.html#exchanging-objects-between-processes
    proc1_pipe, proc2_pipe = multiprocessing.Pipe()

    proc1 = multiprocessing.Process(target=proc1_func, args=(proc1_pipe, ))
    proc2 = multiprocessing.Process(target=proc2_func, args=(proc2_pipe, ))

    proc1.start()
    proc2.start()

    # The main process waits for its children
    proc1.join()
    proc2.join()
    print("exit")

if __name__ == '__main__':
    main()
