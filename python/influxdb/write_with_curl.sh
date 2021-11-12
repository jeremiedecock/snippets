#!/bin/sh

INFLUXDB_ORG="jdhp.org"
INFLUXDB_BUCKET=test
INFLUXDB_HOST="http://localhost:8086"
TOKEN=$(cat INFLUXDB_SECRET_TOKEN)

curl --header "Authorization: Token $TOKEN" --data-raw "cpu,host=serverA,region=uswest idle=10,user=20,system=30 $(date +%s)" "${INFLUXDB_HOST}/api/v2/write?org=${INFLUXDB_ORG}&bucket=${INFLUXDB_BUCKET}&precision=s"
