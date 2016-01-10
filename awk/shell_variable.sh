#!/bin/sh

# Shell variables can be passed to AWK using the -v option.
 
V1=5
V2=10

echo | awk  -v x=$V1  -v y=$V2  '{print x, y}'

