#!/bin/sh

# Only print lines where the value of the 6th column is equal to "1"

awk '$6 == 1 {print $0}' /etc/fstab


# Only print lines where the value of the 3th column is greater than "1000"

awk -F':' '$3 > 1000 {print $0}' /etc/passwd
