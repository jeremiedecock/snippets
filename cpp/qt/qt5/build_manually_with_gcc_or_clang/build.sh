#!/bin/sh

#CC=g++
CC=clang++

# The -fPIC flag seems to be required for Qt5...
$CC -fPIC $(pkg-config --cflags Qt5Widgets) -c hello.cc
$CC -o hello $(pkg-config --libs Qt5Widgets) hello.o

