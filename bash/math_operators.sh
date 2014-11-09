#!/bin/sh

# Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)

X=5
((X = 2 * $X))
echo $X         # -> 10
