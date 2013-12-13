#!/bin/bash

PRINTER_NAME='c24'

FILE=$1

lp -d '${PRINTER_NAME}' -o number-up=2 -o prettyprint "${FILE}"

