#!/bin/sh

# ...IN... | tr "," "_" | ...OUT...

# WARNING:
# "tr" takes the original text in STDIN then transform it and finally sends it to STDOUT

FOO="a,b,c"
echo $FOO

FOO=$(echo $FOO | tr "," "_")
echo $FOO
