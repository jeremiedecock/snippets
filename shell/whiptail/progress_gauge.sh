#!/bin/bash

# Syntax: whiptail --gauge <text> <height> <width> [<percent>]
# Also reads percent from stdin:

{
    for ((i = 0 ; i <= 100 ; i+=5)); do
        sleep 0.1
        echo $i
    done
} | whiptail --gauge "Please wait while we are sleeping..." 6 50 0
