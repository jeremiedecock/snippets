#!/bin/sh

# Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)

# Simple case: cmd1 $(cmd2)  or  cmd1 `cmd2`
# Nested case: cmd1 $(cmd2 $(cmd3))
vim $(grep -l termios $(find . -name "*.cpp"))
