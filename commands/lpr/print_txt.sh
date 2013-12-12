#!/bin/bash

PRINTER_NAME='c24'

for FILE in "$@"
do
    echo "PRINT $FILE"
    lp -d '${PRINTER_NAME}' -o number-up=2 -o prettyprint "${FILE}"
done
