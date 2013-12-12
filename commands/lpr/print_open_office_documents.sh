#!/bin/bash

SOFFICE_RUN=$(ps -e | grep soffice)
echo "Convertion doesn't work if an instance of Libre Office is already running!"

find orig -type f \( -regex ".*\.docx?" -o -regex ".*\.od[ts]" \) -exec soffice --headless --convert-to pdf --outdir ./ "{}" \;

for FILE in *.pdf
do
    echo "PRINT $FILE"
    lp -d 'c24' -o number-up=2 "${FILE}"
done

