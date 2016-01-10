#!/bin/sh

# Print the first column of "uptime"

uptime | awk '{print $1}'


# Print the 2nd and the 4th column of "uptime"

uptime | awk '{print $2, $4}'


# Print the last column of "uptime"

uptime | awk '{print $NF}'

