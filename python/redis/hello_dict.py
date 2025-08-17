#!/usr/bin/env python3

import redis

# Connect to the Redis server running on localhost at port 6379

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Set a key-value pair in Redis

r.hset('user-session:123', mapping={
    'name': 'John',
    "surname": 'Smith',
    "company": 'Redis',
    "age": 29
})

# Retrieve the value of the key 'user-session:123'

response = r.hgetall('user-session:123')

print(f'The value of "user-session:123" is: {response}')