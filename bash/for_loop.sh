#!/bin/bash

# Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)

for FILE in *.sh
do  
    ls -l ${FILE}
done

for FILE in $(find . -type f -name "*.sh")
do  
    ls -l ${FILE}
done
