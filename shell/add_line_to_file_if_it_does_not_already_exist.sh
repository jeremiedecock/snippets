#!/bin/sh

# https://stackoverflow.com/a/3557165

DST_FILE="/media/jeremie/boot/config.txt"
LINE_TO_APPEND="lcd_rotate=2"

grep -qxF ${LINE_TO_APPEND} ${DST_FILE} || echo ${LINE_TO_APPEND} >> ${DST_FILE}
