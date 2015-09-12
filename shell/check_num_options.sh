#!/bin/bash

usage_func() {
    echo "USAGE: $0 hello world"
    exit 1
}

if [ $# -ne 2 ]; then
    echo "Error: wrong number of parameters"
    usage_func
fi

if [ $1 != "hello" ]; then
    echo "Error: first parameter"
    usage_func
fi

if [ $2 != "world" ]; then
    echo "Error: second parameter"
    usage_func
fi

echo "Hello!"
