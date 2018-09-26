#!/bin/sh

# TODO:
# - Add a brief presentation of the library
# - Say there is more than a hundred snippets here

NUM_SNIPPETS=$(find . -type f -name "*.py" | wc -l)

# MAKE TITLE AND MAIN DESCRIPTION #############################################

cat << 'EOF' > README.md
# Matplotlib Snippets

EOF

echo "This directory contains ${NUM_SNIPPETS} Tkinter snippets." >> README.md

cat << 'EOF' >> README.md

## Snippets list

EOF

# LIST SNIPPETS ###############################################################

for PY_FILE in *.py
do
    SNIPPET_BASENAME=$(basename -s ".py" ${PY_FILE})
    SNIPPET_PNG="${SNIPPET_BASENAME}.png"
    SNIPPET_GIF="${SNIPPET_BASENAME}.gif"
    SNIPPET_TITLE=$(echo ${SNIPPET_BASENAME} | tr "_" " ") 
    GITHUB_LINK="https://github.com/jeremiedecock/snippets/tree/master/python/matplotlib/${PY_FILE}"

    # Uppercase the first letter of the title (see https://stackoverflow.com/questions/12487424/uppercase-first-character-in-a-variable-with-bash#12487455)
    SNIPPET_TITLE=$(echo ${SNIPPET_TITLE} | sed 's/./\U&/') 

    if ! test -L "${PY_FILE}"                   # Skip symbolic links
    then
        echo "" >> README.md
        echo "### ${SNIPPET_TITLE}" >> README.md
        echo "" >> README.md

        if test -f "${SNIPPET_GIF}"
        then
            ALT_TEXT="${SNIPPET_GIF}"
            echo "<a href=\"${GITHUB_LINK}\"><img alt=\"${ALT_TEXT}\" title=\"Display the source code\" src=\"${SNIPPET_GIF}\"></a>" >> README.md
        else
            if test -f "${SNIPPET_PNG}"
            then
                ALT_TEXT="${SNIPPET_PNG}"
                echo "<a href=\"${GITHUB_LINK}\"><img alt=\"${ALT_TEXT}\" title=\"Display the source code\" src=\"${SNIPPET_PNG}\"></a>" >> README.md
            else
                echo "<a href=\"${GITHUB_LINK}\">${PY_FILE}</a>" >> README.md
            fi
        fi
    fi
done

# ADDITIONAL DOCUMENTATION ####################################################

cat << 'EOF' >> README.md


EOF
