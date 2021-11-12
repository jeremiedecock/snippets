#!/bin/sh

INFLUXDB_ORG="jdhp.org"
INFLUXDB_BUCKET=test
INFLUXDB_HOST="http://localhost:8086"
TOKEN=$(cat INFLUXDB_SECRET_TOKEN)

influx write --org ${INFLUXDB_ORG} --bucket ${INFLUXDB_BUCKET} --token ${TOKEN} --precision s --host ${INFLUXDB_HOST} "cpu,host=serverA,region=uswest idle=30,user=40,system=10 $(date +%s)"
