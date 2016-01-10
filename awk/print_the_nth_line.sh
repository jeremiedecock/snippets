#!/bin/sh

# Print the first line of "/etc/passwd"

awk 'NR == 1 {print $0}' /etc/passwd


# Print the 2nd and the 4th line of "/etc/passwd"

awk 'NR==2 || NR==4 {print $0}' /etc/passwd


# Print all lines of "/etc/passwd" between the 1st one and the 5th one

awk 'NR==1 , NR==5 {print $0}' /etc/passwd


# Print the last line of "/etc/passwd"

awk 'END {print $0}' /etc/passwd
