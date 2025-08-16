# Redis

See:
- https://redis.io/docs/latest/get-started/
- https://redis.io/docs/latest/develop/clients/redis-py/


## Run a Redis server with Podman

https://hub.docker.com/_/redis

```
podman run -it -p 6379:6379 docker.io/library/redis
```

```
podman run -it -p 6379:6379 docker.io/library/redis:alpine
```

## Installation of redis-py

From this directory:

```
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```