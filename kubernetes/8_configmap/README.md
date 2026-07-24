# ConfigMap

Same FastAPI app as `7_custom_image`, but the returned message is no longer
hard-coded: `main.py` now reads it from the `MESSAGE` environment variable,
and that variable is injected by Kubernetes from a **ConfigMap**.

A ConfigMap stores non-sensitive configuration as key/value pairs, *outside*
the image. This is the point: the exact same image runs unchanged in every
environment (dev, staging, prod...); only the ConfigMap differs.
Configuration is data, not code.

## Build and push version 2.0

`main.py` changed, so a new image version must be built and pushed (details in
`7_custom_image`; same commands with `docker` + `-f Containerfile`):

```
podman build -t docker.io/your-username/hello-fastapi:2.0 .
podman push docker.io/your-username/hello-fastapi:2.0
```

Note that the app keeps a default value (`"hello"`) when the variable is not
set — the image still works on its own, configuration only *overrides*.

## Deploy

Two changes in `deployment.yml` compared to `7_custom_image`: the image tag
(`2.0`), and the `env` block, which fills the `MESSAGE` environment variable
with the `message` key of the `hello` ConfigMap
(`valueFrom.configMapKeyRef`). Edit `your-username`, then:

`kubectl apply -f configmap.yml -f deployment.yml -f service.yml`

Use it: `kubectl port-forward service/hello 8080:80`, then
`curl http://localhost:8080/` → `{"message":"Hello from the ConfigMap!"}`

## Update the configuration

Change the message in `configmap.yml`, re-apply it, and curl again:

```
kubectl apply -f configmap.yml
curl http://localhost:8080/
```

... the message did not change! Environment variables are read once, when the
container starts. The Pods must be restarted to pick up the new value:

```
kubectl rollout restart deployment/hello
```

(then restart the `port-forward` and curl again — this time the new message
shows up.)

Note: a ConfigMap can also be *mounted as files* inside the containers
(`volumes` + `volumeMounts` in the Pod template). With that mode, updates
propagate to running containers after a minute or so, without restart — but
the app must re-read the file to notice.

Delete everything: `kubectl delete -f configmap.yml -f deployment.yml -f service.yml`
