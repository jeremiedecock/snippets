# Psycopg snippets

Official doc: https://www.psycopg.org/docs/usage.html

Comparison of drivers: https://wiki.postgresql.org/wiki/Python

## Run PostgreSQL locally with Podman

1. Ensure you have [Podman](https://podman.io/getting-started/installation) installed on your machine.
2. Run the following command in a terminal to start a PostgreSQL container:

```
./run_psql_server.sh
```

See [Official Docker images on Docker Hub](https://hub.docker.com/_/postgres/) and [its documentation](https://github.com/docker-library/docs/blob/master/postgres/README.md).

## Run the snippets within a VSCode Dev Container

1. Ensure you have the [Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) installed in VSCode.
2. Open this project folder in VSCode.
3. When prompted, reopen the folder in a container.
4. Once the container is running, open a terminal in VSCode and run the following command to execute the FastAPI snippet: `python snippets_name.py` (replace `snippets_name.py` with the actual name of the snippet you want to run).

## Run the snippets locally with Podman (without VSCode Dev Container)

1. Ensure you have [Podman](https://podman.io/getting-started/installation) installed on your machine.
2. Build the Podman image using the provided `Containerfile`. Run the following command in a terminal: `./build.sh` or `podman build -t snippets-psycopg:latest .`
3. Run FastAPI in a Podman container. Run the following command in a terminal: `./run.sh hello.py`
