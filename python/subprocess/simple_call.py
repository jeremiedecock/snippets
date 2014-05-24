#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# see: https://docs.python.org/3.3/library/subprocess.html#module-subprocess

import sys
import subprocess

def main():
    """Main function"""

    # subprocess.call and subprocess.check_output are convenience functions (wrappers).
    # For more advanced use cases, the underlying subprocess.Popen interface
    # can be used directly.

    # WITHOUT ERROR HANDLING ##################################################

    # Test 1: very basic call with an argument and without error handling
    print("TEST1")
    subprocess.call("ls -l", shell=True)  # bad choice
    print()
    subprocess.call(["ls", "-l"])         # good choice
    print()


    # WITH AUTOMATIC ERROR HANDLING ###########################################

    # Test 2a: get output and errors
    print("TEST2A")
    try:
        output = subprocess.check_output(["ls", "."], stderr=subprocess.STDOUT, universal_newlines=True)
        print(output)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print("Execution failed:", e, file=sys.stderr)
        print("Return code:", e.returncode, file=sys.stderr)
        print("Output message:", e.output, file=sys.stderr)
    print()

    # Test 2b: get output and errors
    print("TEST2B")
    try:
        output = subprocess.check_output(["ls", "unknown_file"], stderr=subprocess.STDOUT, universal_newlines=True)
        print(output)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print("Execution failed:", e, file=sys.stderr)
        print("Return code:", e.returncode, file=sys.stderr)
        print("Output message:", e.output, file=sys.stderr)
    print()

    # Test 2c: get output and errors
    print("TEST2C")
    try:
        output = subprocess.check_output(["unknown_cmd"], stderr=subprocess.STDOUT, universal_newlines=True)
        print(output)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print("Execution error:", e, file=sys.stderr)
        print("Return code:", e.returncode, file=sys.stderr)
        print("Output message:", e.output, file=sys.stderr)
    print()


    # WITH MANUAL ERROR HANDLING ##############################################

    # Test 3: when arguments contain space
    print("TEST3")
    try:
        ret_code = subprocess.call(["./test_children/test_child.sh", "hello", "world", "hello world"])

        if ret_code < 0:
            print("Child was terminated by signal", -ret_code, file=sys.stderr)
        else:
            print("Child returned", ret_code, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
    print()


    # Test 4: when child process return an error code != 0 and write on stderr
    print("TEST4")
    try:
        ret_code = subprocess.call(["ls", "unknown_file"])

        if ret_code < 0:
            print("Child was terminated by signal", -ret_code, file=sys.stderr)
        else:
            print("Child returned", ret_code, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
    print()


    # Test 5: when the command is unknown -> exception handling
    print("TEST5")
    try:
        ret_code = subprocess.call(["unknown_command"])

        if ret_code < 0:
            print("Child was terminated by signal", -ret_code, file=sys.stderr)
        else:
            print("Child returned", ret_code, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
    print()


    # Test 6: multiple commands with pipes
    print("TEST6")
    try:
        ret_code = subprocess.call("ls -a -l | ./test_children/test_child_echo_stdin_stdout.sh", shell=True)

        if ret_code < 0:
            print("Child was terminated by signal", -ret_code, file=sys.stderr)
        else:
            print("Child returned", ret_code, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
    print()


    # Test 7: when the command doesn't return immediately
    print("TEST7")
    try:
        ret_code = subprocess.call("sleep 1 && echo \"timeout\"", shell=True)

        if ret_code < 0:
            print("Child was terminated by signal", -ret_code, file=sys.stderr)
        else:
            print("Child returned", ret_code, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
    print()


    # Test 8: with timeout
    print("TEST8")
    try:
        ret_code = subprocess.call(["sleep", "10"], timeout=1) # timeout=1sec

        if ret_code < 0:
            print("Child was terminated by signal", -ret_code, file=sys.stderr)
        else:
            print("Child returned", ret_code, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
    except subprocess.TimeoutExpired as e:
        print("Execution stopped:", e, file=sys.stderr)
    print()

if __name__ == '__main__':
    main()
