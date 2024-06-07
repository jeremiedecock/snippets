# CouchDB


## Documentation

- https://couchdb.apache.org/
- https://hub.docker.com/_/couchdb
- https://github.com/apache/couchdb-docker


## Run a server with Docker

Set `COUCHDB_USER` and `COUCHDB_PASSWORD` environment variables (e.g. in `.bashrc`) then type:

```
docker run --name couchdb-server --rm -e COUCHDB_USER=${COUCHDB_USER} -e COUCHDB_PASSWORD=${COUCHDB_PASSWORD} -p 5984:5984 couchdb:3.3.3
```

or provide credentials directly in the `docker run` command (not recommended):

```
docker run --name couchdb-server --rm -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=password -p 5984:5984 couchdb:3.3.3
```


## Run a server with DockerCompose

```
docker-compose up -d
```