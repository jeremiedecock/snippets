#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jeremie Decock (http://www.jdhp.org)

# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.

# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# TODO: improve this script
# - safer method to reading and convert data to int
# - fix warnings
# - let matplotlib be less stressful for CPU

import numpy as np
import matplotlib.pyplot as plt

import argparse
import serial
import time

X_DELTA = 1
TIME_SLEEP = 0.1
MAX_VALUES = 50
Y_MIN = 0
Y_MAX = 1024

def main():

    # PARSE OPTIONS

    parser = argparse.ArgumentParser(description='A pyserial snippet.')

    parser.add_argument("--baudrate", "-b",  help="The baudrate speed (e.g. 9600)", metavar="INTEGER", type=int, default=9600)
    parser.add_argument("--timeout", "-t",  help="The timeout value for the connection", metavar="FLOAT", type=float, default=0.1)
    parser.add_argument("--port", "-p",  help="The serial device to connect with (e.g. '/dev/ttyUSB0' for Unix users)", metavar="STRING", default="/dev/ttyUSB0")
    args = parser.parse_args()

    # CONNECT TO THE SERIAL PORT

    serial_connection = serial.Serial(port=args.port,
                                      baudrate=args.baudrate,
                                      timeout=args.timeout,
                                      bytesize=serial.EIGHTBITS,
                                      parity=serial.PARITY_NONE,
                                      stopbits=serial.STOPBITS_ONE)

    serial_connection.flushInput()
    
    # INIT PLOT

    plt.ion()    # setup interactive mode
    plt.show()

    x_vec = []
    y_vec = []

    x_value = 0

    # READ DATA

    while(True):
        time.sleep(TIME_SLEEP)

        # READ DATA
        read_byte_array = serial_connection.read(7)
        if len(read_byte_array) > 0:
            current_value = int(read_byte_array)

            print(current_value )

            # PLOT
            x_vec.append(x_value)
            y_vec.append(current_value)

            if len(x_vec) > MAX_VALUES:
                x_vec.pop(0)
                y_vec.pop(0)

            plt.clf()

            plt.xlim(x_vec[0], x_vec[-1])
            plt.ylim(Y_MIN, Y_MAX)

            plt.plot(x_vec, y_vec, "-")
            plt.draw()

            x_value += X_DELTA


if __name__ == '__main__':
    main()
