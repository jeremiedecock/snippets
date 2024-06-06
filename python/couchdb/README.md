# CouchDB


C.f.

- https://couchdb.apache.org/
- https://hub.docker.com/_/couchdb
- https://github.com/apache/couchdb-docker



docker run --name my-couchdb -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=password -p 5984:5984 couchdb:3.3.3

curl http://127.0.0.1:5984/

curl -X GET http://admin:password@127.0.0.1:5984/_all_dbs

curl -X PUT http://admin:password@127.0.0.1:5984/test

curl -X POST -H "Content-Type: application/json" http://admin:password@127.0.0.1:5984/test -d '{ "in" : {"i1":1, "i2":2}, "out": {"o1":1, "o2":2} }'

curl -X POST -H "Content-Type: application/json" http://admin:password@127.0.0.1:5984/test -d '{ "in" : {"i1":11, "i2":22}, "out": {"o1":11, "o2":22} }'

curl -X PUT http://admin:password@127.0.0.1:5984/test/_design/myview -d '{"views":{"my_filter":{"map": "function(doc) { if(doc.in && doc.in.i1 && doc.out) { emit(doc.in.i1, doc.out); }}"}}}'

curl -X GET http://admin:password@127.0.0.1:5984/test/_design/myview/_view/my_filter
