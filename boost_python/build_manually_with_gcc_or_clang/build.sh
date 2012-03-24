#!/bin/sh

CC=g++
#CC=clang++

$CC -fPIC -c func.cc
$CC -fPIC -I/usr/include/python2.7 -c python_wrapper.cc

# if python's module is named X ("import X"), then shared library have to be named X.so
$CC -shared -o cppfunc.so func.o python_wrapper.o -lboost_python

