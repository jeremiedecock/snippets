#!/bin/sh

# Usage example:
# ./test_child.sh hello world "hello world"

echo "Hello, args are:"

for ARGVAL in "$@"
do
    echo "${ARGVAL}"
done

