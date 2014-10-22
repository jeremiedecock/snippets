#!/bin/sh

CC=g++

$CC -fopenmp -c hello.cc
$CC -fopenmp hello.o

