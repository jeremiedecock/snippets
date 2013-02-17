#!/bin/bash

FOO="HELLO"
BAR="WORLD"
export BAR

echo "FROM THE SCRIPT:"
echo "FOO=$FOO"
echo "BAR=$BAR"
echo

echo "FROM A CHILD OF THE SCRIPT:"
env | grep "FOO"
env | grep "BAR"

