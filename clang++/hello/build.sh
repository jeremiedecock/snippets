#!/bin/sh

CC=clang++

$CC -Wall -pedantic -g -c hello.cc
$CC -o hello hello.o

