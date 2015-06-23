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

import argparse
import serial
import time

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

    # READ DATA

    while(True):
        time.sleep(0.01)

        num_bytes_in_read_buffer = serial_connection.inWaiting()
        read_byte_array = serial_connection.read(num_bytes_in_read_buffer)
        if len(read_byte_array) > 0:
            print(read_byte_array)


if __name__ == '__main__':
    main()
