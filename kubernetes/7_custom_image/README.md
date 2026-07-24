# Custom image (FastAPI)

Every example so far deployed a stock nginx image. This one deploys **your own
application**: a minimal API built with
[FastAPI](https://fastapi.tiangolo.com/) — a single file (`main.py`) with a
single route returning a "hello" message. The Kubernetes side goes back to the
simple `3_deployment` layout (Deployment + Service, `kubectl port-forward`) to
stay focused on the image workflow.

Kubernetes cannot use an image that only exists on your machine: the cluster
nodes *pull* images from a registry (Docker Hub, quay.io, GitHub Container
Registry...). The workflow is always: **build** the image → **push** it to a
registry → **reference** it in the YAML.

## 1. Build the image

The recipe is in `Containerfile` — "Containerfile" is the tool-neutral,
standard name for what Docker calls a "Dockerfile" (same syntax): official
base image with Python, install FastAPI, copy `main.py`, start the server on
port 8000.

With [Podman](https://podman.io/), which looks for a `Containerfile` by
default (replace `your-username` with your Docker Hub username here and
everywhere below):

```
podman build -t docker.io/your-username/hello-fastapi:1.0 .
```

With Docker, which looks for a `Dockerfile`, the file must be named
explicitly:

```
docker build -f Containerfile -t docker.io/your-username/hello-fastapi:1.0 .
```

Test the image locally before pushing it (`docker run` works the same):

```
podman run --rm -p 8000:8000 docker.io/your-username/hello-fastapi:1.0
```

then `curl http://localhost:8000/` → `{"message":"hello"}`.

Note: if your machine and the cluster nodes have different CPU architectures
(e.g. building on an ARM Mac for an x86 cluster), add
`--platform linux/amd64` to the build command.

## 2. Push it to a registry

Log in once, then push (same commands with `docker`):

```
podman login docker.io
podman push docker.io/your-username/hello-fastapi:1.0
```

To use [quay.io](https://quay.io/) instead of Docker Hub, simply replace
`docker.io` with `quay.io` everywhere (including in the image tag, which is
why the registry is part of the tag).

Check on the registry's website that the repository is **public**: a private
repository requires an image pull Secret
(`kubectl create secret docker-registry`) referenced in the Deployment's
`spec.template.spec.imagePullSecrets` — Secrets are covered in `9_secret_base64`.

Alternative without any registry, for local clusters only: load the image
straight into the cluster (`minikube image load ...` or
`kind load docker-image ...`) and set `imagePullPolicy: Never` in the
Deployment.

## 3. Deploy it

Compared to `3_deployment`, only `deployment.yml` changes:

- `image:` points to your repository — **edit it** to replace
  `your-username`;
- `containerPort` is `8000` (FastAPI's server) instead of `80`. Since
  `service.yml` targets the container port by its *name* (`http`), the
  Service itself does not change at all.

Deploy everything: `kubectl apply -f deployment.yml -f service.yml`

Use it: `kubectl port-forward service/hello 8080:80`, then
`curl http://localhost:8080/` → `{"message":"hello"}` (FastAPI also serves
interactive docs at `http://localhost:8080/docs`)

See the app logs: `kubectl logs -f deployment/hello`

To ship a new version of the app: rebuild with a **new tag** (`1.1`), push,
update `image:` in `deployment.yml` and re-apply — Kubernetes performs a
rolling update (see `3_deployment`). Avoid reusing a tag (or the implicit
`latest`): Kubernetes could not tell the versions apart, and rollbacks would
become meaningless.

Delete everything: `kubectl delete -f deployment.yml -f service.yml`
