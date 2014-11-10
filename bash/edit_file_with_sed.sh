#!/bin/sh

# Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)

sed -i "s/^OPTION1=OFF$/OPTION=ON/" test.txt
sed -i "s/^#OPTION2=\"\"$/OPTION2=\"blablabla\"/" test.txt

