# Fullstack: two services communicating

A minimal fullstack app, to show how two services talk to each other inside
the cluster:

- **backend** — the FastAPI API from the previous examples (the plain `1.0`
  image built in `7_custom_image`: nothing to rebuild);
- **frontend** — an nginx Pod serving a single HTML page
  (`frontend/index.html`): a button triggers a `fetch("/api/")` and displays
  the returned message.

Each component gets its own Deployment and its own ClusterIP Service (grouped
in `backend.yml` and `frontend.yml` — a single YAML file can hold several
resources, separated by `---`).

## How the two services communicate

The browser runs *outside* the cluster: it cannot resolve cluster Service
names. So the page calls its own origin (`/api/`), and the frontend's nginx
*proxies* that path to the backend (see `frontend/default.conf`):

```
location /api/ {
    proxy_pass http://backend/;
}
```

`backend` here is simply the name of the backend **Service**: as seen in
`2_clusterip_service`, every Service gets a stable internal DNS name. That
name works from any Pod in the same namespace (from another namespace it
would be `backend.<namespace>`, e.g. `backend.default`).

The full chain: browser → frontend Service → nginx Pod → backend Service →
FastAPI Pod (each Service load-balancing across its replicas). Bonus of the
same-origin proxy: no CORS configuration needed. (An alternative would be to
expose both Services through the Gateway of `4_gateway_api`, with one
HTTPRoute rule per path.)

## Build and push the frontend image

From the `frontend/` directory (details in `7_custom_image`; same commands
with `docker` + `-f Containerfile`):

```
cd frontend
podman build -t docker.io/your-username/hello-frontend:1.0 .
podman push docker.io/your-username/hello-frontend:1.0
```

## Deploy

Edit `your-username` in both YAML files, then:

`kubectl apply -f backend.yml -f frontend.yml`

Use it: `kubectl port-forward service/frontend 8080:80`, then open
`http://localhost:8080` in a web browser and click the button — the message
`hello` produced by the backend appears on the page.

You can also check the internal chain by hand, from inside the cluster:

```
kubectl run test --rm -it --restart=Never --image=curlimages/curl -- curl -s http://backend/
kubectl run test --rm -it --restart=Never --image=curlimages/curl -- curl -s http://frontend/api/
```

Delete everything: `kubectl delete -f backend.yml -f frontend.yml`
