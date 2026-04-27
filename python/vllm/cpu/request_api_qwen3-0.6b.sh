#!/bin/bash

curl http://127.0.0.1:8080/v1/models

echo ""
echo ""

curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen3-0.6B",
    "messages": [
      {"role": "system", "content": "Tu es un assistant utile et concis."},
      {"role": "user", "content": "Explique-moi ce qu'\''est un LLM en 3 phrases."}
    ]
  }'

echo ""

# curl http://127.0.0.1:8080/v1/chat/completions \
#   -H "Content-Type: application/json" \
#   -d '{
#     "model": "Qwen/Qwen3-0.6B",
#     "stream": true,
#     "messages": [
#       {"role": "system", "content": "Tu es un assistant utile et concis."},
#       {"role": "user", "content": "Explique-moi ce qu'\''est un LLM en 3 phrases."}
#     ]
#   }'
