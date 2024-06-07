#!/usr/bin/env python3

import requests
import json
import os


DB_LOGIN = os.getenv('COUCHDB_USER')          # 'admin'
DB_PASSWORD = os.getenv('COUCHDB_PASSWORD')   # 'password'
DB_ADDRESS = '127.0.0.1'
DB_PORT = '5984'

DB_URL = f'http://{DB_LOGIN}:{DB_PASSWORD}@{DB_ADDRESS}:{DB_PORT}'
DB_NAME = 'my_db'
DB_VIEW = 'my_view'
DB_FILTER = 'my_filter'


# Print general information about the server ##################################

# curl http://127.0.0.1:5984/
response = requests.get(f'{DB_URL}/')
print(response.text)


# Delete a database ###########################################################

# curl -X DELETE http://${COUCHDB_USER}:${COUCHDB_PASSWORD}@127.0.0.1:5984/plankton
response = requests.delete(f'{DB_URL}/{DB_NAME}')
print(response.text)


# List all databases ##########################################################

# curl -X GET http://${COUCHDB_USER}:${COUCHDB_PASSWORD}@127.0.0.1:5984/_all_dbs
response = requests.get(f'{DB_URL}/_all_dbs')
print(response.text)


# Create a database ###########################################################

# curl -X PUT http://${COUCHDB_USER}:${COUCHDB_PASSWORD}@127.0.0.1:5984/test
response = requests.put(f'{DB_URL}/{DB_NAME}')
print(response.text)


# Push documents ##############################################################

# curl -X POST -H "Content-Type: application/json" http://${COUCHDB_USER}:${COUCHDB_PASSWORD}@127.0.0.1:5984/test -d '{ "in" : {"i1":1, "i2":2}, "out": {"o1":1, "o2":2} }'
headers = {'Content-Type': 'application/json'}
data = json.dumps({"in" : {"i1":1, "i2":2}, "out": {"o1":1, "o2":2}})
response = requests.post(f'{DB_URL}/{DB_NAME}', headers=headers, data=data)
print(response.text)

# curl -X POST -H "Content-Type: application/json" http://${COUCHDB_USER}:${COUCHDB_PASSWORD}@127.0.0.1:5984/test -d '{ "in" : {"i1":11, "i2":22}, "out": {"o1":11, "o2":22} }'
data = json.dumps({"in" : {"i1":11, "i2":22}, "out": {"o1":11, "o2":22}})
response = requests.post(f'{DB_URL}/{DB_NAME}', headers=headers, data=data)
print(response.text)


# Query the database ##########################################################

# Create a view
# curl -X PUT http://${COUCHDB_USER}:${COUCHDB_PASSWORD}@127.0.0.1:5984/test/_design/myview -d '{"views":{"my_filter":{"map": "function(doc) { if(doc.in && doc.in.i1 && doc.out) { emit(doc.in.i1, doc.out); }}"}}}'
data = json.dumps({"views":{DB_FILTER:{"map": "function(doc) { if(doc.in && doc.in.i1 && doc.out) { emit(doc.in.i1, doc.out); }}"}}})
response = requests.put(f'{DB_URL}/{DB_NAME}/_design/{DB_VIEW}', headers=headers, data=data)
print(response.text)

# Query the view
# curl -X GET http://${COUCHDB_USER}:${COUCHDB_PASSWORD}@127.0.0.1:5984/test/_design/myview/_view/my_filter
response = requests.get(f'{DB_URL}/{DB_NAME}/_design/{DB_VIEW}/_view/{DB_FILTER}')
print(response.text)
print(response.json())
