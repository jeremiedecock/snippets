# Confluent Kafka Python Client

See: https://docs.confluent.io/kafka-clients/python/current/overview.html


## Installation

From this directory:

```
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

## Usage

...

## Podman

### Build the Podman image

```
./build.sh
```

or

```
podman build -t snippets-kafka-python-client:latest .
```

### Run a script using the Podman image

```
./run.sh python3 produce_message.py
```

or 

```
podman run --rm -it -v .:/app -w /app -u $(id -u):$(id -g) --userns=keep-id localhost/snippets-kafka-python-client:latest python3 produce_message.py
```
