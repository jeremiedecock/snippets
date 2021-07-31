#!/bin/bash

source ../../env/bin/activate

pyside6-uic bookwindow.ui > ui_bookwindow.py
pyside6-rcc books.qrc > rc_books.py

python3 main.py

rm ui_bookwindow.py
rm rc_books.py

rm -rf __pycache__
