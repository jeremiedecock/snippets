# Ray

https://docs.ray.io/


## Installation

From this directory:

```
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```


## Usage

`./hello.py`


## Podman

### Build the Podman image

```
./build.sh
```

or

```
podman build -t snippets-ray-core:latest .
```

### Run a script using the Podman image

```
./run.sh hello.py
```

or 

```
podman run --rm -it -v .:/app -w /app -u $(id -u):$(id -g) --userns=keep-id --network=host localhost/snippets-ray-core:latest python3 hello.py
```
