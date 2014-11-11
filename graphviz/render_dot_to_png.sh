#!/bin/bash

for FILE in "$@"
do
    # http://stackoverflow.com/questions/407184/how-to-determine-file-type-in-bash-script
    if [[ "$FILE" == *.dot ]]
    then
        ls "${FILE}"
        PNG_FILE="$(basename "${FILE}" .dot).png"
        dot -Tpng "${FILE}" > "${PNG_FILE}"
    else
        echo "Error: ${FILE} is not a dot file."
    fi
done
