#!/usr/bin/env python3

import requests
import json

import requests

# curl -X DELETE http://admin:password@127.0.0.1:5984/plankton
response = requests.delete('http://admin:password@127.0.0.1:5984/test')
print(response.text)

# curl http://127.0.0.1:5984/
response = requests.get('http://127.0.0.1:5984/')
print(response.text)

# curl -X GET http://admin:password@127.0.0.1:5984/_all_dbs
response = requests.get('http://admin:password@127.0.0.1:5984/_all_dbs')
print(response.text)

# curl -X PUT http://admin:password@127.0.0.1:5984/test
response = requests.put('http://admin:password@127.0.0.1:5984/test')
print(response.text)

# curl -X POST -H "Content-Type: application/json" http://admin:password@127.0.0.1:5984/test -d '{ "in" : {"i1":1, "i2":2}, "out": {"o1":1, "o2":2} }'
headers = {'Content-Type': 'application/json'}
data = json.dumps({"in" : {"i1":1, "i2":2}, "out": {"o1":1, "o2":2}})
response = requests.post('http://admin:password@127.0.0.1:5984/test', headers=headers, data=data)
print(response.text)

# curl -X POST -H "Content-Type: application/json" http://admin:password@127.0.0.1:5984/test -d '{ "in" : {"i1":11, "i2":22}, "out": {"o1":11, "o2":22} }'
data = json.dumps({"in" : {"i1":11, "i2":22}, "out": {"o1":11, "o2":22}})
response = requests.post('http://admin:password@127.0.0.1:5984/test', headers=headers, data=data)
print(response.text)

# curl -X PUT http://admin:password@127.0.0.1:5984/test/_design/myview -d '{"views":{"my_filter":{"map": "function(doc) { if(doc.in && doc.in.i1 && doc.out) { emit(doc.in.i1, doc.out); }}"}}}'
data = json.dumps({"views":{"my_filter":{"map": "function(doc) { if(doc.in && doc.in.i1 && doc.out) { emit(doc.in.i1, doc.out); }}"}}})
response = requests.put('http://admin:password@127.0.0.1:5984/test/_design/myview', headers=headers, data=data)
print(response.text)

# curl -X GET http://admin:password@127.0.0.1:5984/test/_design/myview/_view/my_filter
response = requests.get('http://admin:password@127.0.0.1:5984/test/_design/myview/_view/my_filter')
print(response.text)
print(response.json())
