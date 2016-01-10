#!/bin/sh

# This snippet shows how to use regular expressions in AWK.
# For instance, here, only the result lines of "ps aux" containing the word "bash" are printed.

ps aux | awk '$0 ~ /bash/ {print $0}'

# or

ps aux | awk '/bash/ {print $0}'
