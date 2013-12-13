#!/bin/bash

# Print .od[st] and .docx? files

SOFFICE_RUN=$(ps -e | grep soffice)
echo "Convertion doesn't work if an instance of Libre Office is already running!"

FILE=$1
PRINTER_NAME='c24'

soffice --headless --convert-to pdf --outdir /tmp/ "${FILE}"

lp -d '${PRINTER_NAME}' -o number-up=2 "/tmp/${FILE}.pdf"

