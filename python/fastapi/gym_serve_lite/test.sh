#!/bin/sh

echo "Reset environments:"
curl -X 'POST' 'http://127.0.0.1:8000/api/reset' -H 'accept: application/json' -H 'Authorization: Bearer token_abc123' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/reset' -H 'accept: application/json' -H 'Authorization: Bearer token_def456' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/reset' -H 'accept: application/json' -H 'Authorization: Bearer token_ghi789' -d '' && echo ""
echo ""
echo ""

echo "Steps:"
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=0' -H 'accept: application/json' -H 'Authorization: Bearer token_abc123' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=0' -H 'accept: application/json' -H 'Authorization: Bearer token_abc123' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=0' -H 'accept: application/json' -H 'Authorization: Bearer token_abc123' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=0' -H 'accept: application/json' -H 'Authorization: Bearer token_abc123' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=0' -H 'accept: application/json' -H 'Authorization: Bearer token_abc123' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=0' -H 'accept: application/json' -H 'Authorization: Bearer token_abc123' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=0' -H 'accept: application/json' -H 'Authorization: Bearer token_abc123' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=0' -H 'accept: application/json' -H 'Authorization: Bearer token_abc123' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=0' -H 'accept: application/json' -H 'Authorization: Bearer token_abc123' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=0' -H 'accept: application/json' -H 'Authorization: Bearer token_abc123' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=0' -H 'accept: application/json' -H 'Authorization: Bearer token_abc123' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=0' -H 'accept: application/json' -H 'Authorization: Bearer token_abc123' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=0' -H 'accept: application/json' -H 'Authorization: Bearer token_abc123' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=0' -H 'accept: application/json' -H 'Authorization: Bearer token_abc123' -d '' && echo ""

echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=2' -H 'accept: application/json' -H 'Authorization: Bearer token_def456' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=2' -H 'accept: application/json' -H 'Authorization: Bearer token_def456' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=2' -H 'accept: application/json' -H 'Authorization: Bearer token_def456' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=2' -H 'accept: application/json' -H 'Authorization: Bearer token_def456' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=2' -H 'accept: application/json' -H 'Authorization: Bearer token_def456' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=2' -H 'accept: application/json' -H 'Authorization: Bearer token_def456' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=2' -H 'accept: application/json' -H 'Authorization: Bearer token_def456' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=2' -H 'accept: application/json' -H 'Authorization: Bearer token_def456' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=2' -H 'accept: application/json' -H 'Authorization: Bearer token_def456' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=2' -H 'accept: application/json' -H 'Authorization: Bearer token_def456' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=2' -H 'accept: application/json' -H 'Authorization: Bearer token_def456' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=2' -H 'accept: application/json' -H 'Authorization: Bearer token_def456' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=2' -H 'accept: application/json' -H 'Authorization: Bearer token_def456' -d '' && echo ""
curl -X 'POST' 'http://127.0.0.1:8000/api/step?action=2' -H 'accept: application/json' -H 'Authorization: Bearer token_def456' -d '' && echo ""

# # Simulate concurrent increments from the same user
# curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_ghi789' -d '' &
# curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_ghi789' -d '' &
# curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_ghi789' -d '' &
# curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_ghi789' -d '' &
# curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_ghi789' -d '' &
# curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_ghi789' -d '' &
# curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_ghi789' -d '' &
# curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_ghi789' -d '' &
# curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_ghi789' -d '' &
# curl -X 'POST' 'http://127.0.0.1:8000/api/counter/increment' -H 'accept: application/json' -H 'Authorization: Bearer token_ghi789' -d '' &
# wait
# echo ""
# echo ""

curl -X 'GET' 'http://127.0.0.1:8000/api/render' -H 'accept: application/json' -H 'Authorization: Bearer token_abc123' --output render.png