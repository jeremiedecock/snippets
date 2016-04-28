#!/bin/bash

# Debian package required:
# - aptitude install cups-pdf
#   (see http://terokarvinen.com/2011/print-pdf-from-command-line-cups-pdf-lpr-p-pdf)
#
# The default output directory is ~/PDF/
#
# lpr options:
# - see http://www.cups.org/documentation.php/doc-1.3/options.html
# - The available printer options vary depending on the printer. The standard
#   options are described in the "Standard Printing Options" section below.
#   Printer-specific options are also available and can be listed using the
#   lpoptions command:
#   lpoptions -p printer -l
# - the -o fitplot option specifies that the document should be scaled to fit
#   on the page
# - Selecting Even or Odd Pages
#   Use the -o page-set=set option to select the even or odd pages:
#   lp -o page-set=odd filename
#   lp -o page-set=even filename
# - The -o landscape option will rotate the page 90 degrees to print in
#   landscape orientation
# - The -o number-up=value option selects N-Up printing. N-Up printing places
#   multiple document pages on a single printed page. CUPS supports 1, 2, 4, 6,
#   9, and 16-Up formats; the default format is 1-Up
#
# List printer names that lpr can understand:
# - lpstat -p -d

PRINTER_NAME="PDF"

FILE="slides_notes.pdf"

cp "${FILE}" /tmp/odd.pdf
cp "${FILE}" /tmp/even.pdf

lpr -P "${PRINTER_NAME}" -o landscape -o fitplot -o page-set=odd /tmp/odd.pdf
lpr -P "${PRINTER_NAME}" -o landscape -o fitplot -o page-set=even /tmp/even.pdf
#mv "~/PDF/${FILE}" ./

echo "Output file: ~/PDF/${FILE}"
echo "Please wait few seconds for the output file generation..."

