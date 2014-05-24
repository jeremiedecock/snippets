#!/bin/sh

# Usage examples:
# ./test_child_echo_stdin_stdout.sh
# ./test_child_echo_stdin_stdout.sh < test_input_file.txt

# Translate (upper case: a->A, b->B, ...) from standard input, writing to standard output.
tr a-z A-Z

