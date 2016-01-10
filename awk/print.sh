#!/bin/sh

# This snippet prints something like "* username : {1} - uid : {3}" for each
# line of /etc/passwd (where {1} and {3} are the value of the 1st and the 3rd
# columns)

awk -F ':' '{print "* username :", $1, "- uid :", $3}' /etc/passwd

