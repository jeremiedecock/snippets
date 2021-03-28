#!/usr/bin/env python3

import pymongo
import datetime

from privateconfig import *

URL = "mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority".format(USER, PASSWORD, HOST, DATABASE)

client = pymongo.MongoClient(URL)

db = client.foo
collection = db.bar


# INSERT A DOCUMENT

personDocument = {
    "name": { "first": "Alan", "last": "Turing" },
    "birth": datetime.datetime(1912, 6, 23),
    "death": datetime.datetime(1954, 6, 7),
    "contribs": [ "Turing machine", "Turing test", "Turingery" ],
    "views": 1250000
}

collection.insert_one(personDocument)


# READ A COLLECTION

res = collection.find_one({ "name.last": "Turing" })

print(res)
