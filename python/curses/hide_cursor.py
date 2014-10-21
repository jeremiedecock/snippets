#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# For more infos on curses, see:
# - https://docs.python.org/3/library/curses.html
# - https://docs.python.org/dev/howto/curses.html

import curses

def main(stdscr):
    """Main function"""

    # Let the cursor be invisible
    curses.curs_set(False)

    # Clear screen
    stdscr.clear()

    # Print a message
    stdscr.addstr('Hello, press any key to quit.')

    # Display the message
    stdscr.refresh()

    # Wait for a key
    stdscr.getkey()

if __name__ == '__main__':

    # A common problem when debugging a curses application is to get your
    # terminal messed up when the application dies without restoring the
    # terminal to its previous state. In Python this commonly happens when your
    # code is buggy and raises an uncaught exception. Keys are no longer echoed
    # to the screen when you type them, for example, which makes using the
    # shell difficult.
    # Use curses.wrapper() to avoid these difficulties. The callable is called
    # inside a try...except that catches exceptions, restores the state of the
    # terminal, and then re-raises the exception. Therefore your terminal won't
    # be left in a funny state on exception and you'll be able to read the
    # exception's message and traceback.
    # This wrapper also initializes curses at the beginning of the callable
    # object given in argument and restore the original state of the terminal
    # when the end.
    curses.wrapper(main)

