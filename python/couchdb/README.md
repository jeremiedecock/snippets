# CouchDB


## Documentation

- https://couchdb.apache.org/
- https://hub.docker.com/_/couchdb
- https://github.com/apache/couchdb-docker
- https://docs.couchdb.org/en/stable/api/ddoc/index.html


## Run a server with Docker

Set `COUCHDB_USER` and `COUCHDB_PASSWORD` environment variables (e.g. in `.bashrc`) then type:

```
docker run --name couchdb-server --rm -e COUCHDB_USER=${COUCHDB_USER} -e COUCHDB_PASSWORD=${COUCHDB_PASSWORD} -p 5984:5984 -v couchdb-data:/opt/couchdb/data couchdb:3.3.3
```

or provide credentials directly in the `docker run` command (not recommended):

```
docker run --name couchdb-server --rm -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=password -p 5984:5984 -v couchdb-data:/opt/couchdb/data couchdb:3.3.3
```


## Run a server with DockerCompose

Set `COUCHDB_JDHP_SNIPPETS_USER` and `COUCHDB_JDHP_SNIPPETS_PASSWORD` environment variables (e.g. in `.bashrc`) then type:

```
docker-compose up
```

or if you want to "detach" the process:

```
docker-compose up -d
```


### Use the Fauxton (CoudhDB's graphical interface)

To load Fauxton in your browser, visit http://127.0.0.1:5984/_utils/
