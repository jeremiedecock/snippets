#!/bin/sh

OUTPUT_FILE="${1:-snippetsdb.dump}"

podman exec \
    -t \
    postgres-sqlmodel-snippets \
    pg_dump -U user -d snippetsdb -F c -f "/tmp/snippetsdb.dump"

podman cp \
    postgres-sqlmodel-snippets:/tmp/snippetsdb.dump \
    "$OUTPUT_FILE"

echo "Database dumped to: $OUTPUT_FILE"
