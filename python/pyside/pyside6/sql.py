#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ref: http://katecpp.github.io/sqlite-with-qt/

from PySide6.QtSql import QSqlDatabase, QSqlQuery


db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName(":memory:")                  # SQLITE DATABASE IN MEMORY
#db.setDatabaseName("./employee.db")            # SQLITE DATABASE FROM FILE
assert db.open()

query = QSqlQuery()


# CREATE TABLE ########################

assert query.exec("CREATE TABLE employee(id NTEGER PRIMARY KEY, first_name VARCHAR, last_name VARCHAR)"), query.lastError()


# INSERT VALUES #######################

query.prepare("INSERT INTO employee(first_name, last_name) VALUES(?, ?)")

query.addBindValue("Jean")
query.addBindValue("Dupont")
assert query.exec(), query.lastError()

query.addBindValue("Paul")
query.addBindValue("Dupond")
assert query.exec(), query.lastError()

query.prepare("INSERT INTO employee(first_name, last_name) VALUES(:first_name, :last_name)")

query.bindValue(":first_name", "Marie")
query.bindValue(":last_name", "Dupuis")
assert query.exec(), query.lastError()

query.bindValue(":first_name", "Alice")
query.bindValue(":last_name", "Martin")
assert query.exec(), query.lastError()

# UPDATE ##############################

assert query.prepare("UPDATE employee SET first_name = (:new_first_name), last_name = (:new_last_name) WHERE first_name = (:old_first_name) AND last_name = (:old_last_name)"), query.lastError()

query.bindValue(":old_first_name", "Jean")
query.bindValue(":old_last_name", "Dupont")
query.bindValue(":new_first_name", "JeanJean")
query.bindValue(":new_last_name", "Dudupont")
assert query.exec(), query.lastError()


# SELECT ##############################

# PRINT ALL EMPLOYEES

query = QSqlQuery("SELECT * FROM employee")

first_name_index = query.record().indexOf("first_name")
last_name_index = query.record().indexOf("last_name")

while query.next():
    print(query.value(first_name_index), query.value(last_name_index))

# CHECK IF PERSON WITH SPECIFIC NAME EXISTS

query.prepare("SELECT first_name FROM employee WHERE first_name = (:first_name)");

query.bindValue(":first_name", "Alice");
assert query.exec(), query.lastError()

if query.next():
    print("At least one employee is named Alice")
else:
    print("Nobody is named Alice")


query.bindValue(":first_name", "Billy");
assert query.exec(), query.lastError()

if query.next():
    print("At least one employee is named Billy")
else:
    print("Nobody is named Billy")


# DELETE ##############################

# DELETE ONE PERSON

query.prepare("DELETE FROM employee WHERE first_name = (:first_name)")
query.bindValue(":first_name", "Dupond")
assert query.exec(), query.lastError()

# DELETE ALL PERSONS

assert query.prepare("DELETE FROM employee"), query.lastError()
