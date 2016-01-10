#!/bin/sh

# This snippet shows how to change the columns (fields) separator.
# For instance, columns 1 and 3 of /etc/passwd are printed here (columns are separated with the ':' character)

awk -F':' '{print $1, $3}' /etc/passwd
