#!/bin/sh

CC=clang++

# WITH PKG-CONFIG
#$CC `pkg-config --cflags QtGui` -c hello.cc
#$CC hello.o `pkg-config --libs QtGui`

# WITHOUT PKG-CONFIG
$CC -DQT_SHARED -I/usr/include/qt4 -I/usr/include/qt4/QtGui -I/usr/include/qt4/QtCore -c hello.cc
$CC hello.o -lQtGui -lQtCore

