#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref: http://doc.qt.io/qt-5/modelview.html#2-1-a-read-only-table

import sys
from PySide6 import QtCore, QtWidgets

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QTableView
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from datetime import date


def add_book(q, title, year, authorId, genreId, rating):
    q.addBindValue(title)
    q.addBindValue(year)
    q.addBindValue(authorId)
    q.addBindValue(genreId)
    q.addBindValue(rating)
    q.exec()

def add_genre(q, name):
    q.addBindValue(name)
    q.exec()
    return q.lastInsertId()

def add_author(q, name, birthdate):
    q.addBindValue(name)
    q.addBindValue(str(birthdate))
    q.exec()
    return q.lastInsertId()

BOOKS_SQL = """
    create table books(id integer primary key, title varchar, author integer,
                       genre integer, year integer, rating integer)
    """
AUTHORS_SQL = """
    create table authors(id integer primary key, name varchar, birthdate text)
    """
GENRES_SQL = """
    create table genres(id integer primary key, name varchar)
    """
INSERT_AUTHOR_SQL = """
    insert into authors(name, birthdate) values(?, ?)
    """
INSERT_GENRE_SQL = """
    insert into genres(name) values(?)
    """
INSERT_BOOK_SQL = """
    insert into books(title, year, author, genre, rating)
                values(?, ?, ?, ?, ?)
    """

def init_db():
    def check(func, *args):
        if not func(*args):
            raise ValueError(func.__self__.lastError())

    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(":memory:")

    check(db.open)

    q = QSqlQuery()
    check(q.exec, BOOKS_SQL)
    check(q.exec, AUTHORS_SQL)
    check(q.exec, GENRES_SQL)
    check(q.prepare, INSERT_AUTHOR_SQL)

    asimovId = add_author(q, "Isaac Asimov", date(1920, 2, 1))
    greeneId = add_author(q, "Graham Greene", date(1904, 10, 2))
    pratchettId = add_author(q, "Terry Pratchett", date(1948, 4, 28))

    check(q.prepare, INSERT_GENRE_SQL)
    sfiction = add_genre(q, "Science Fiction")
    fiction = add_genre(q, "Fiction")
    fantasy = add_genre(q, "Fantasy")

    check(q.prepare, INSERT_BOOK_SQL)
    add_book(q, "Foundation", 1951, asimovId, sfiction, 3)
    add_book(q, "Foundation and Empire", 1952, asimovId, sfiction, 4)
    add_book(q, "Second Foundation", 1953, asimovId, sfiction, 3)
    add_book(q, "Foundation's Edge", 1982, asimovId, sfiction, 3)
    add_book(q, "Foundation and Earth", 1986, asimovId, sfiction, 4)
    add_book(q, "Prelude to Foundation", 1988, asimovId, sfiction, 3)
    add_book(q, "Forward the Foundation", 1993, asimovId, sfiction, 3)
    add_book(q, "The Power and the Glory", 1940, greeneId, fiction, 4)
    add_book(q, "The Third Man", 1950, greeneId, fiction, 5)
    add_book(q, "Our Man in Havana", 1958, greeneId, fiction, 4)
    add_book(q, "Guards! Guards!", 1989, pratchettId, fantasy, 3)
    add_book(q, "Night Watch", 2002, pratchettId, fantasy, 3)
    add_book(q, "Going Postal", 2004, pratchettId, fantasy, 3)


app = QApplication(sys.argv)

init_db()

table_view = QTableView()

model = QSqlQueryModel()
model.setQuery("SELECT * FROM books")

table_view.setModel(model)
table_view.show()

# The mainloop of the application. The event handling starts from this point.
exit_code = app.exec()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
