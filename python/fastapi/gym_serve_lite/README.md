# FastAPI Hello World

## Run the Application within a VSCode Dev Container

1. Ensure you have the [Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) installed in VSCode.
2. Open this project folder in VSCode.
3. When prompted, reopen the folder in a container.
4. Once the container is built and running, you can start the FastAPI server. Run the following command in the terminal inside the container: `fastapi dev main.py`
5. Open your browser and navigate to `http://localhost:8000` to see the FastAPI application running. You can also access the interactive API documentation at `http://localhost:8000/docs`.

## Run the Application Locally with Podman

1. Ensure you have [Podman](https://podman.io/getting-started/installation) installed on your machine.
2. Build the Podman image using the provided `Containerfile`. Run the following command in a terminal: `./build.sh` or `podman build -t snippets-fastapi:latest .`
3. Run FastAPI in a Podman container. Run the following command in a terminal: `./run.sh` or `podman run --rm -it -v .:/app -w /app -u $(id -u):$(id -g) --userns=keep-id -p 8000:8000 localhost/snippets-fastapi:latest` or `podman run --rm -it -v .:/app -w /app -u $(id -u):$(id -g) --userns=keep-id -p 8000:8000 localhost/snippets-fastapi:latest fastapi dev main.py --host 0.0.0.0 --port 8000`
4. Open your browser and navigate to `http://localhost:8000` to see the FastAPI application running. You can also access the interactive API documentation at `http://localhost:8000/docs`.

## Testing the Authentication

You can test this snippet with the following command:

```
curl -X 'GET' 'http://127.0.0.1:8000/api/counter' -H 'accept: application/json' -H 'Authorization: Bearer token_abc123'
```

or

```
python3 client.py
```

See `test.sh` for more example commands.

## Warning

This snippet stores state in memory (a Python dictionary) inside the server process.
That means the state is **not shared** across multiple worker processes.

In practice, if you run with `--workers > 1` (or behind a process manager that forks multiple workers), each worker will have its own independent counters. Requests from the same client may hit different workers (depending on your load balancing / scheduling), so the counter can appear to “reset”, jump, or behave inconsistently.

Also note that development features like auto-reload restart the process regularly, which will wipe the in-memory state.

To run this snippet with a single worker (and without auto-reload), use: `fastapi run main.py --host 0.0.0.0 --port 8000 --workers 1 --no-reload`.
For real deployments that need shared, durable, or horizontally scalable state, use an external store (e.g., Redis or a database) instead of in-memory globals.
