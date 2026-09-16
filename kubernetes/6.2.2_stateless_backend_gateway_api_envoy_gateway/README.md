# Your own image, exposed with the Gateway API (Envoy Gateway)

This is [`6.2.1_stateless_backend_ingress_traefik`](../6.2.1_stateless_backend_ingress_traefik/)
with the **Ingress replaced by the Gateway API**: the same FastAPI image from
[`6.1_private_docker_registry`](../6.1_private_docker_registry/), the same
Deployment, the same ClusterIP Service — and a **Gateway** plus an
**HTTPRoute** in front of it instead of a single Ingress object.

The Ingress API is feature-frozen, and its most popular controller,
ingress-nginx, was retired in March 2026. The
[Gateway API](https://gateway-api.sigs.k8s.io/) is its official successor, so
**this is the version to use for new work** — 6.2.1 remains useful because
existing clusters are full of Ingress manifests.

Everything about the Gateway API itself is explained in
[`4.3.1_gateway_api_envoy_gateway`](../4.3.1_gateway_api_envoy_gateway/),
which did exactly this with a stock nginx image. Read it first if the three
resources below are new to you: this directory reuses its `gateway.yml`,
`gateway-class.yml` and installation steps verbatim, and only changes what is
*behind* the Gateway.

## What is in this directory

| File | What it is |
| --- | --- |
| `main.py`, `Containerfile` | the same app and the same build as 6.1, unchanged (FastAPI pinned to one version, so that two builds of a tag cannot differ) |
| `deployment.yml` | a Deployment of the GHCR image, with `imagePullSecrets`, a named port `http` and a readiness probe |
| `service.yml` | a ClusterIP Service, `port: 80` → `targetPort: http` |
| `gateway-class.yml` | the `eg` GatewayClass, binding class name → Envoy Gateway controller (cluster-wide) |
| `gateway.yml` | a Gateway with one `HTTP:80` listener — identical to 4.3.1's |
| `http-route.yml` | an HTTPRoute attaching to that Gateway and sending everything to `my-service` |
| `secret.yml` | the pull Secret as a manifest — for reference, not to be applied (see 6.1) |

`deployment.yml` and `service.yml` are byte-for-byte those of 6.2.1, so
applying this example after that one is a rolling update of the same app, not
a second copy of it. The image is the one built in 6.1 — same repository, same
`1.0` tag, same `main.py` — so if it is still on GHCR, steps 1 and 2 below are
a no-op and you can jump to *3. Create the namespace and the pull Secret*.

## What changes compared to `6.2.1`

| | `6.2.1` (Ingress) | `6.2.2` (here, Gateway API) |
| --- | --- | --- |
| Routing objects | one `Ingress` | a `GatewayClass`, a `Gateway`, an `HTTPRoute` |
| Controller | Traefik | Envoy Gateway |
| API group | `networking.k8s.io/v1` | `gateway.networking.k8s.io/v1` |
| Which controller handles it | `spec.ingressClassName` | `spec.gatewayClassName`, on the Gateway |
| Where the address appears | on the `Ingress` | on the `Gateway` (`ADDRESS` column) |
| The proxy's Service | `service/traefik`, in the release's namespace | generated in `envoy-gateway-system` |
| Advanced routing | controller-specific **annotations** | typed fields (`filters`, header matching, weights...) |
| Cross-namespace routing | not expressible | explicit, via `ReferenceGrant` |
| Status when misconfigured | often silence | conditions on each object: `Accepted`, `ResolvedRefs`, `Programmed` |

The last two rows are why the Gateway API exists. An Ingress that no
controller claims simply stays empty, with nothing to read; here, every object
carries status conditions saying whether it was accepted, and why not.

## The split, and why it matters

The Ingress crammed the entry point *and* the routing rules into one object,
with anything beyond a hostname and a path pushed into vendor-specific
annotations. The Gateway API splits the same job across three resources,
each meant for a different owner:

| Resource | Answers | Typically owned by |
| --- | --- | --- |
| `GatewayClass` | which implementation handles traffic? | the cluster administrator, once per cluster |
| `Gateway` | what listens, on which port and protocol? | the cluster/platform operator |
| `HTTPRoute` | which requests go to which Service? | the application developer |

In this demo you play all three roles, which flattens the point — so notice
the shape rather than the ceremony: **one Gateway is shared**, and each app
adds its own HTTPRoute to it, in its own namespace, without touching the
Gateway. That is what
[`4.3.2_gateway_api_envoy_gateway_multi_apps`](../4.3.2_gateway_api_envoy_gateway_multi_apps/)
demonstrates with two apps, and what a single Ingress per app cannot express.

The chain is otherwise the one from 6.2.1:

```
browser --HTTP--> Gateway (Envoy proxy) ----> Service "my-service" --> Pod
                       ^                          ^                   (FastAPI,
              gateway.yml: listener :80    service.yml: port 80        :8000)
              http-route.yml: -> Service        -> targetPort http
```

### The port chain, again

Unchanged from 6.2.1, and still the most common source of silent failures.
`backendRefs[].port` in the HTTPRoute is the **Service** port, not the
container port:

| Where | Field | Value |
| --- | --- | --- |
| `deployment.yml` | `containerPort` | `8000`, named `http` |
| `service.yml` | `targetPort` | `http` (the name, resolved per Pod) |
| `service.yml` | `port` | `80` — what the Service answers on |
| `http-route.yml` | `backendRefs[].port` | `80` — must equal the Service's `port` |

The Service port and the container port are deliberately different, so that
the distinction is visible rather than hidden behind two identical numbers.

### `imagePullSecrets` in a Pod template

Same trap as in 6.2.1, worth repeating because it is the one thing that
differs from 6.1's bare Pod: `imagePullSecrets` belongs to the **Pod spec**
nested in the Deployment's `template`, next to `containers:` — not next to
`replicas:`.

### The readiness probe

`deployment.yml` carries one, on `/`. Without it, a Pod counts as ready as
soon as its container process exists, so the Service starts routing to it
before uvicorn is listening — a handful of `503`s at every rollout, for no
visible reason. The kubelet queries the probe from the Pod's own IP and cannot
authenticate, so an app that demands a password everywhere needs a dedicated
unauthenticated health path instead.

## Prerequisites

- **A container engine** — [Podman](https://podman.io/) below; `docker` works
  identically, with `-f Containerfile` added to the build.
- **A GitHub account**, for GHCR.
- **A cluster whose LoadBalancer Services get an address.** Envoy Gateway
  provisions one for the Gateway, and its address is the entry point. On a
  local cluster this needs MetalLB, `minikube tunnel`,
  `cloud-provider-kind` or equivalent; without it the Gateway's `ADDRESS`
  never appears.
- **Envoy Gateway and the `eg` GatewayClass**, installed as in
  [4.3.1's prerequisites](../4.3.1_gateway_api_envoy_gateway/README.md#prerequisite-a-gateway-api-implementation)
  — including the checks to make *before* installing anything cluster-wide.
  See step 4 below for the short version.

Replace `jeremiedecock` with your own GitHub username, here and in
`deployment.yml`:

```shell
sed -i 's/jeremiedecock/your-github-username/g' deployment.yml
```

## 1. Create a Personal Access Token

If 6.1 or 6.2.1 is still fresh, `$GHCR_TOKEN` is set and you are logged in —
skip to step 2.

Otherwise create a **PAT (classic)**, as described in
[Authenticating with a personal access token](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-with-a-personal-access-token-classic),
with the scopes `read:packages`, `write:packages`, `delete:packages` and
`repo`. The cluster only ever needs `read:packages`; the rest are for you.
Keep it in your `.bashrc`:

```shell
export GHCR_TOKEN=ghp_...
```

Then log in, with the token on stdin so it stays out of your shell history:

```shell
echo $GHCR_TOKEN | podman login ghcr.io -u jeremiedecock --password-stdin
```

## 2. Build and push the image

Same image and same tag as 6.1 and 6.2.1 — see
[Pushing container images](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#pushing-container-images):

```shell
podman build -t ghcr.io/jeremiedecock/hello-fastapi:1.0 .
```

Optional, and the cheapest way to rule the app out of any later problem:

```shell
podman run -p 8000:8000 ghcr.io/jeremiedecock/hello-fastapi:1.0
```

Open `http://localhost:8000` for the FastAPI welcome message, or
`http://localhost:8000/docs` for the generated documentation. `Ctrl+C` stops
it.

```shell
podman push ghcr.io/jeremiedecock/hello-fastapi:1.0
```

Check the pushed image at <https://github.com/jeremiedecock?tab=packages> —
it is **private**, hence the next step.

## 3. Create the namespace and the pull Secret

```shell
kubectl create namespace snippet-backend-gatewayapi-demo
```

Add `-n snippet-backend-gatewayapi-demo` to every `kubectl` command below.

The Secret is detailed in
[6.1](../6.1_private_docker_registry/#4-create-the-pull-secret); in short, it
wraps the token in the `dockerconfigjson` format the kubelet expects, and
`deployment.yml` names it in `imagePullSecrets`:

```shell
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username='jeremiedecock' \
  --docker-password="$GHCR_TOKEN" \
  -n snippet-backend-gatewayapi-demo
```

That `-n` is not optional: a pull Secret is a **namespaced** object, and the
kubelet only looks for it in the namespace of the Pod that references it. A
Secret in `default` is invisible to a Pod anywhere else.

```shell
kubectl get secret ghcr-secret -n snippet-backend-gatewayapi-demo
```

## 4. Install Envoy Gateway and the GatewayClass

Both the Gateway API CRDs and their controller are **cluster-wide and
shared**, so check before installing anything. Empty output or a `NotFound`
means absent:

```shell
kubectl api-resources --api-group=gateway.networking.k8s.io
kubectl get deployments -n envoy-gateway-system
helm list --all-namespaces
```

If they are already there, skip the `helm install` and go straight to the
GatewayClass check. Otherwise, install the controller — which brings the CRDs
with it:

```shell
helm install eg oci://docker.io/envoyproxy/gateway-helm --version v1.9.1 -n envoy-gateway-system --create-namespace
kubectl wait --timeout=5m -n envoy-gateway-system deployment/envoy-gateway --for=condition=Available
```

Then the GatewayClass. It is cluster-wide too, so again, look first:

```shell
kubectl get gatewayclass
```

If an entry already has `gateway.envoyproxy.io/gatewayclass-controller` in its
`CONTROLLER` column, reuse it: put its name in `spec.gatewayClassName` of
`gateway.yml` and skip the apply. Otherwise:

```shell
kubectl apply -f gateway-class.yml
```

`ACCEPTED` must read `True` — `False` or `Unknown` means the controller is not
running:

```shell
kubectl get gatewayclass
```

Another implementation (Cilium, Istio, Traefik, Kong, NGINX Gateway
Fabric...) works just as well: `gateway.yml` and `http-route.yml` are standard
objects, and only the GatewayClass's `controllerName` is implementation-specific.

## 5. Deploy the app

```shell
kubectl apply -f deployment.yml -f service.yml -f gateway.yml -f http-route.yml \
  -n snippet-backend-gatewayapi-demo
```

Wait for the image to be pulled from GHCR and the readiness probe to pass:

```shell
kubectl rollout status deployment/my-deployment -n snippet-backend-gatewayapi-demo
```

Then wait for the Gateway. Envoy Gateway reacts by creating an Envoy proxy
Deployment and a LoadBalancer Service for it, in `envoy-gateway-system`, so
`PROGRAMMED=True` and a populated `ADDRESS` take a moment (`Ctrl+C` to stop
watching):

```shell
kubectl get gateway -n snippet-backend-gatewayapi-demo --watch
```

The generated proxy, which you never wrote and never manage directly:

```shell
kubectl get all -n envoy-gateway-system
```

Before going outside, check the two hops the route depends on. The Service
must have an endpoint — empty means no Pod is ready, or its `selector` does
not match the Pods:

```shell
kubectl get endpointslices -l kubernetes.io/service-name=my-service \
  -n snippet-backend-gatewayapi-demo
```

(`kubectl get endpoints my-service` shows the same thing more compactly, but
the Endpoints API is deprecated in favour of EndpointSlice since Kubernetes
1.33.)

And the HTTPRoute must have been **accepted by the Gateway and have resolved
its backend**. This is the Gateway API's real advantage over Ingress: the
answer is written down rather than inferred from a `404`:

```shell
kubectl describe httproute my-route -n snippet-backend-gatewayapi-demo
```

Look for two conditions under `Parents`:

```
Accepted        True    Route is accepted
ResolvedRefs    True    Resolved all the Object references for the Route
```

`ResolvedRefs: False` with `BackendNotFound` means `backendRefs` names a
Service that does not exist (or is in another namespace, which needs a
`ReferenceGrant`). `Accepted: False` with `NoMatchingParent` means
`parentRefs` does not match the Gateway.

## 6. Test it

```shell
ADDR=$(kubectl get gateway my-gateway -n snippet-backend-gatewayapi-demo \
  -o jsonpath='{.status.addresses[0].value}')
echo $ADDR
```

One field is enough here, unlike 6.2.1's Ingress: the Gateway API normalises
the address into a `value` plus a `type` (`IPAddress` or `Hostname`), so the
same `jsonpath` works on every provider. `kubectl get gateway -o yaml` shows
the `type` if you are curious which one you got.

`gateway.yml`'s listener declares **no `hostname`**, and `http-route.yml` has
no `hostnames:` either, so any host matches and the bare address works:

```shell
curl http://$ADDR/
```

```json
{"message":"hello"}
```

The commented-out `matches:` block in `http-route.yml` is the explicit form of
what happens by default — a rule with no `matches` matches every path. Add it
back, and path-based routing becomes a typed field rather than an annotation:

```yaml
matches:
  - path:
      type: PathPrefix
      value: /
```

FastAPI's generated documentation comes through the same route:

```shell
curl http://$ADDR/openapi.json
```

Open `http://<ADDRESS>/docs` in a browser for the Swagger UI.

Optionally, point a DNS `A` record at that address and use the name instead;
nothing in the manifests changes, and it is the prerequisite for a real
certificate later.

**No HTTPS here, at all.** Unlike 6.2.1 — where the Traefik chart may answer
on 443 with a default self-signed certificate — this Gateway declares a single
`HTTP:80` listener, so nothing listens on 443 and `https://` simply fails to
connect. Adding a listener is [`5.1_tls`](../5.1_tls/) (by hand) and
[`5.2_lets_encrypt`](../5.2_lets_encrypt/) (automatically); this app gets a
real certificate in
[`6.3`](../6.3_stateless_backend_gateway_api_envoy_gateway_with_lets_encrypt/).

## Scaling and updating

Same as 6.2.1, and worth trying once — neither the Gateway nor the HTTPRoute
is touched by any of it:

```shell
kubectl scale deployment/my-deployment --replicas=3 -n snippet-backend-gatewayapi-demo
for i in $(seq 6); do curl -s http://$ADDR/ > /dev/null; done
kubectl logs -l app=my-app --prefix --tail=3 -n snippet-backend-gatewayapi-demo
```

```shell
podman build -t ghcr.io/jeremiedecock/hello-fastapi:1.0.1 .
podman push ghcr.io/jeremiedecock/hello-fastapi:1.0.1
kubectl set image deployment/my-deployment \
  my-container=ghcr.io/jeremiedecock/hello-fastapi:1.0.1 \
  -n snippet-backend-gatewayapi-demo
kubectl rollout status deployment/my-deployment -n snippet-backend-gatewayapi-demo
```

`my-container=` is the **container** name from `deployment.yml`, and the new
tag matters: overwriting `1.0` would change what every other demo in the
series pulls. `kubectl rollout undo deployment/my-deployment` reverts. Scale
back down before moving on:

```shell
kubectl scale deployment/my-deployment --replicas=1 -n snippet-backend-gatewayapi-demo
```

## When it does not work

Read the status conditions from the outside in — Gateway, HTTPRoute, Service,
Pods. Each object says what it is unhappy about:

```shell
kubectl describe gateway my-gateway -n snippet-backend-gatewayapi-demo
kubectl describe httproute my-route -n snippet-backend-gatewayapi-demo
kubectl get endpointslices -l kubernetes.io/service-name=my-service -n snippet-backend-gatewayapi-demo
kubectl describe pod -l app=my-app -n snippet-backend-gatewayapi-demo | tail -20
```

- **The Gateway has no `ADDRESS`, `PROGRAMMED` stays `False`.** Either no
  controller is reconciling it — `gatewayClassName` does not match an
  `ACCEPTED` GatewayClass, or the controller is not running — or the cluster
  has no LoadBalancer provider, in which case the proxy Service in
  `envoy-gateway-system` sits at `<pending>`.
- **`404` from Envoy.** The request reached the proxy and matched no route.
  `kubectl describe httproute my-route` will show `Accepted: False`
  (`NoMatchingParent`: `parentRefs` names the wrong Gateway, or the listener
  restricts which namespaces may attach), or you are querying a hostname the
  route does not cover.
- **`503`.** The route matched, the backend has nothing behind it.
  `ResolvedRefs: False` / `BackendNotFound` means a wrong Service name or
  port in `backendRefs` (`80` here, not `8000`); a resolved ref with an empty
  `endpointslices` listing means no Pod is ready, or `service.yml`'s
  `selector` does not match `deployment.yml`'s labels.
- **Pods in `ImagePullBackOff` / `ErrImagePull`.** The registry side, as in
  6.1. A `401` in the Pod events means the Secret is missing, misnamed in
  `imagePullSecrets`, **in another namespace**, or built with a
  `--docker-server` other than exactly `ghcr.io`.
- **Pods `Running` but `0/1 READY`.** The readiness probe is failing;
  `kubectl describe pod -l app=my-app` gives the status code it got.
- **Pods `CrashLoopBackOff`.** Not Kubernetes: `kubectl logs -l app=my-app`
  has the app's traceback. Listening on `127.0.0.1` instead of `0.0.0.0` is
  the classic one.

## Remove the demo

```shell
kubectl delete -f http-route.yml -f gateway.yml -f service.yml -f deployment.yml \
  -n snippet-backend-gatewayapi-demo
kubectl delete namespace snippet-backend-gatewayapi-demo
```

Deleting the namespace takes the `ghcr-secret` Secret with it. Deleting the
Gateway is what removes the generated Envoy proxy and its LoadBalancer
Service — check that it went away, since on a cloud provider it costs money:

```shell
kubectl get all -n envoy-gateway-system
```

### Shared cluster add-ons: stop and check first

The GatewayClass and the Envoy Gateway controller are cluster-wide and
shared. **Do not delete them if you did not install them, or if anything else
still uses them.** List every Gateway on the cluster first; if any remains,
leave both in place:

```shell
kubectl get gateway --all-namespaces \
  -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,CLASS:.spec.gatewayClassName'
```

If nothing else uses them:

```shell
kubectl delete -f gateway-class.yml
helm uninstall eg --namespace envoy-gateway-system
```

**Keep the image.** `hello-fastapi:1.0` is this app — `{"message": "hello"}`,
documentation enabled — and 6.4 expects exactly that content behind the tag.
The later examples add their own tags rather than overwriting it (`1.0.1` for
the rolling update in this example, `4.0` and `5.0` for the persistence
chapters).

When you are done with the series, revoke the PAT from *Settings → Developer
settings → Personal access tokens* and clear the local credentials with
`podman logout ghcr.io`.
