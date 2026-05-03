#!/bin/sh

if [ -z "$1" ]; then
    echo "\nUsage: $0 <dump_file>\n"
    exit 1
fi

podman cp \
    "$1" \
    postgres:/tmp/snippetsdb.dump

podman exec \
    -t \
    postgres \
    pg_restore -U user -d snippetsdb --clean --if-exists -F c /tmp/snippetsdb.dump

echo "Database restored from: $1"
