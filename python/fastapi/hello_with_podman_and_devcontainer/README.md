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
3. Run FastAPI in a Podman container. Run the following command in a terminal: `./run.sh fastapi dev main.py --host 0.0.0.0` or `podman run --rm -it -v .:/app -w /app -u $(id -u):$(id -g) --userns=keep-id -p 8000:8000 localhost/snippets-fastapi:latest`
4. Open your browser and navigate to `http://localhost:8000` to see the FastAPI application running. You can also access the interactive API documentation at `http://localhost:8000/docs`.
