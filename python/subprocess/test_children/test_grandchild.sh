#!/bin/sh

sleep 30 &
echo $!
sleep 30 &
echo $!
sleep 30 &
echo $!
ps -jH
wait
