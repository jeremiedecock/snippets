#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# see: https://docs.python.org/3.3/library/subprocess.html#module-subprocess

import sys
import subprocess

def main():
    """Main function"""

    process = subprocess.Popen(["./test_children/test_child_echo_stdin_stdout.sh"], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines=True)

    out, err = process.communicate("abc\n")
    print(out)


if __name__ == '__main__':
    main()
