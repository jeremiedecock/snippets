#!/bin/sh

if [ -z "$1" ]; then
    echo "\nUsage: $0 <table_name>\n"
    echo "The list of available tables can be obtained with: run_psql_list_tables.sh\n"
    exit 1
fi

podman exec \
    -it \
    postgres-sqlmodel-snippets \
    psql -U user -d snippetsdb -c "SELECT * FROM $1;"
