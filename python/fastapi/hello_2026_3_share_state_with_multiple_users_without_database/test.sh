#!/bin/sh

echo "Reset counters:"
curl -X 'POST' 'http://127.0.0.1:8000/api/counter/reset' -H 'accept: application/json' -H 'Authorization: Bearer token_abc123' -d ''
curl -X 'POST' 'http://127.0.0.1:8000/api/counter/reset' -H 'accept: application/json' -H 'Authorization: Bearer token_def456' -d ''
curl -X 'POST' 'http://127.0.0.1:8000/api/counter/reset' -H 'accept: application/json' -H 'Authorization: Bearer token_ghi789' -d ''
echo ""
echo ""

echo "Increment counters:"
# curl -X 'GET' 'http://127.0.0.1:8000/api/counter' -H 'accept: application/json' -H 'Authorization: Bearer token_abc123'

# curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_abc123' -d ''
# curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_abc123' -d ''
# curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_abc123' -d ''

# curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_def456' -d ''
# curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_def456' -d ''
# curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_def456' -d ''

# Simulate concurrent increments from the same user
curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_ghi789' -d '' &
curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_ghi789' -d '' &
curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_ghi789' -d '' &
curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_ghi789' -d '' &
curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_ghi789' -d '' &
curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_ghi789' -d '' &
curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_ghi789' -d '' &
curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_ghi789' -d '' &
curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_ghi789' -d '' &
curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_ghi789' -d '' &
wait
echo ""
echo ""

echo "Final counter values:"
curl -X 'GET' 'http://127.0.0.1:8000/api/counter' -H 'accept: application/json' -H 'Authorization: Bearer token_ghi789'
echo ""