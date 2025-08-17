#!/usr/bin/env python3

import asyncio
import redis.asyncio as redis


async def main():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    print(f"Ping successful: {await r.ping()}")
    await r.aclose()


if __name__ == "__main__":
    asyncio.run(main())
