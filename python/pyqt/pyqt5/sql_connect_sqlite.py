#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# https://doc.qt.io/qtforpython/PySide2/QtSql/QSqlDatabase.html
# https://doc.qt.io/qt-5/sql-programming.html
# https://www.developpez.net/forums/d1590644/autres-langages/python/gui/pyqt/qtsql-probleme-setquery/

# TO MAKE THE TEST DATABASE
# -------------------------
# $ sqlite3 test.sqlite
# sqlite> CREATE TABLE t_pers (nom VARCHAR, age INTEGER);
# sqlite> INSERT INTO t_pers VALUES ("john", 30);
# sqlite> INSERT INTO t_pers VALUES ("billy", 25);

from PyQt5 import QtSql

db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("test.sqlite")

if not db.open():
    db = None # Erreur d'ouverture de la base de données basesql

#query = QtSql.QSqlQuery("SELECT * FROM t_pers", db)

query = QtSql.QSqlQuery()
query.exec("SELECT * FROM t_pers")

while query.next():
    name = query.value(0)      # QString
    age = query.value(1)
    print(name, age)
