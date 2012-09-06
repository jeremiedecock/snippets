#!/bin/sh

CC=clang

$CC -Wall -pedantic -g -c hello.c
$CC -o hello hello.o

