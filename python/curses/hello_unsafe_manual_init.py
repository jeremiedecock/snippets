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

def main():
    """Main function"""

    # INIT ################################################

    # Determine the terminal type, send any required setup codes to the
    # terminal, and create various internal data structures.
    # This returns a window object representing the entire screen.
    stdscr = curses.initscr()

    # Turn off automatic echoing of keys to the screen.
    curses.noecho()

    # React to keys instantly, without requiring the Enter key to be pressed.
    curses.cbreak()

    # Terminals usually return special keys, such as the cursor keys or
    # navigation keys such as Page Up and Home, as a multibyte escape sequence.
    # While you could write your application to expect such sequences and
    # process them accordingly, curses can do it for you, returning a special
    # value such as curses.KEY_LEFT. To get curses to do the job, you’ll have
    # to enable keypad mode.
    stdscr.keypad(True)

    # APP'S CODE ##########################################

    # Clear screen
    stdscr.clear()

    # Print a message
    stdscr.addstr('Hello, press any key to quit.')

    # Display the message
    stdscr.refresh()

    # Wait for a key
    stdscr.getkey()

    # QUIT ################################################

    # Reverse the curses-friendly terminal settings.
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()

    # Restore the terminal to its original operating mode
    curses.endwin()

if __name__ == '__main__':

    main()

