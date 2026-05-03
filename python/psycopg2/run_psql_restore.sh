#!/bin/sh

if [ -z "$1" ]; then
    echo "\nUsage: $0 <dump_file>\n"
    exit 1
fi

podman cp \
    "$1" \
    postgres-psycopg2-snippets:/tmp/snippetsdb.dump

podman exec \
    -t \
    postgres-psycopg2-snippets \
    pg_restore -U user -d snippetsdb --clean --if-exists -F c /tmp/snippetsdb.dump

echo "Database restored from: $1"
