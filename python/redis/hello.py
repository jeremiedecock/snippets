#!/usr/bin/env python3

import redis

# Connect to the Redis server running on localhost at port 6379

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Set a key-value pair in Redis

r.set('foo', 'bar')

# Retrieve the value of the key 'foo'

response = r.get('foo')

print(f'The value of "foo" is: {response}')