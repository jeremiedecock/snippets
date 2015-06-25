#!/bin/sh

SYS_GPIO=/sys/class/gpio

# Gain access to GPIO 24 (pin 18)
echo 24 > ${SYS_GPIO}/export

echo out > ${SYS_GPIO}/gpio24/direction

# Switch ON the LED
echo 1 > ${SYS_GPIO}/gpio24/value

sleep 1

# Switch OFF the LED
echo 0 > ${SYS_GPIO}/gpio24/value

echo 24 > ${SYS_GPIO}/unexport
