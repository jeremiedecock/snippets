# Your own image, exposed to the internet (Traefik Ingress)

[`6.1_private_docker_registry`](../6.1_private_docker_registry/) got your own
image running in the cluster, but only reachable through
`kubectl port-forward` — a debugging tool, not a way to publish a service.
Here the same FastAPI image is **exposed to the internet**, by putting back
the three layers the earlier chapters introduced one at a time:

- a **Deployment** ([`3.2_deployment`](../3.2_deployment/)) instead of the
  bare Pod, so the app is supervised, replicable and updatable;
- a **ClusterIP Service** ([`2.1_clusterip_service`](../2.1_clusterip_service/))
  to give it a stable internal address;
- an **Ingress** ([`4.2_ingress_traefik`](../4.2_ingress_traefik/)) handled by
  the Traefik controller, to route outside traffic to that Service.

Nothing in that list is new. What this directory adds is the combination —
and the three details that only show up once a **private image** meets a
**Deployment**: where `imagePullSecrets` goes in a Pod *template*, how the port
number travels from the browser down to `containerPort: 8000`, and why a
Deployment serving real traffic wants a readiness probe.

[`6.2.2_stateless_backend_gateway_api_envoy_gateway`](../6.2.2_stateless_backend_gateway_api_envoy_gateway/)
is this same example with the **Gateway API** in place of the Ingress, which
is what new projects should use; this one is worth doing first, because the
Ingress version is shorter and is still what you will meet in existing
clusters.

## What is in this directory

| File | What it is |
| --- | --- |
| `main.py`, `Containerfile` | the same app and the same build as 6.1, unchanged (FastAPI pinned to one version, so that two builds of a tag cannot differ) |
| `deployment.yml` | a Deployment of the GHCR image, with `imagePullSecrets`, a named port `http` and a readiness probe |
| `service.yml` | a ClusterIP Service, `port: 80` → `targetPort: http` |
| `ingress.yml` | an Ingress with `ingressClassName: traefik`, routing `/` to that Service |
| `secret.yml` | the pull Secret as a manifest — for reference, not to be applied (see 6.1) |

The image is the one built in 6.1 — same repository, same `1.0` tag, same
`main.py`. If you still have it on GHCR, steps 1 and 2 below are a no-op and
you can jump to *3. Create the namespace and the pull Secret*; the build
instructions are repeated here so that this directory stands on its own.

## The chain, end to end

```
browser --HTTP--> Traefik ---------> Service "my-service" --> Pod
                  (LoadBalancer      (ClusterIP,             (FastAPI,
                   Service, :80)      port 80)                :8000)
                     ^                    ^                     ^
          ingress.yml names the      service.yml maps       deployment.yml
          Service and its port       port -> targetPort     names the port
```

Four port declarations have to line up, and a mismatch in any of them fails
*silently* — with a `404` or a `503` rather than an error at `apply` time.
Read them in this order:

| Where | Field | Value | Means |
| --- | --- | --- | --- |
| `deployment.yml` | `containerPort` | `8000` | the port FastAPI listens on, named `http` |
| `service.yml` | `targetPort` | `http` | *the name*, resolved per Pod (cf. [`2.2`](../2.2_clusterip_service_with_named_port/)) |
| `service.yml` | `port` | `80` | the port the **Service** answers on, inside the cluster |
| `ingress.yml` | `backend.service.port.number` | `80` | must match the Service's `port`, **not** the container's |

The last row is the classic trap: the Ingress talks to the *Service*, so the
number it carries is the Service's port. The two are deliberately different
here — `80` on the Service, `8000` in the container — precisely so that the
distinction is visible. Change `service.yml`'s `port` to `8000` and only
`ingress.yml` has to follow; the container is unaware of any of it.

Note also that `containerPort` is **documentation**, not a binding: the app
listens on 8000 because the `Containerfile` tells `fastapi run` to, and
declaring it here is what lets the Service refer to it by name.

## Where `imagePullSecrets` goes

This is the one thing that catches everybody moving from 6.1's Pod to a
Deployment. `imagePullSecrets` is a field of a **Pod spec**, and a Deployment
does not have one — it has a Pod *template* that contains one:

```yaml
spec:                       # Deployment spec
  template:
    spec:                   # Pod spec: this is the one
      containers: [...]
      imagePullSecrets:
        - name: ghcr-secret
```

Put it one level too high, next to `replicas:`, and the API server rejects it
outright (`unknown field`), which is the good case. The bad case is putting it
at the right level but with the wrong Secret name, or in the wrong namespace:
everything applies cleanly, and the Pods sit in `ImagePullBackOff`.

Same rule, same place, for the `containers:` list itself — which is why
`deployment.yml` looks deeper than 6.1's `pod.yml` while saying nearly the
same thing.

## The readiness probe

`deployment.yml` adds one, and it is not decoration. A Pod with no probe is
considered ready as soon as its container *process* exists, so the Service
adds it to its endpoints while uvicorn is still starting up — which surfaces
as a handful of `503`s at every rollout, and as a demo that fails
intermittently for no visible reason.

```yaml
readinessProbe:
  httpGet:
    path: /
    port: http
  periodSeconds: 10
```

`/` is enough for this app: it is cheap, and it needs no credentials. That
last point matters more than it looks — the kubelet queries the probe from the
Pod's own IP and cannot be taught to authenticate, so an app that requires a
password on every path needs a dedicated unauthenticated health path instead.
`5.3.2` makes the same point from the other side, with `auth_basic off` on
`/healthz`.

## Prerequisites

- **A container engine** — [Podman](https://podman.io/) below; `docker` works
  identically, with `-f Containerfile` added to the build.
- **A GitHub account**, for GHCR.
- **A Kubernetes cluster whose Services of type `LoadBalancer` get an
  address.** This is the real constraint of this example: Traefik is exposed
  through such a Service, and on a cloud cluster its `EXTERNAL-IP` is a public
  address. On a local cluster it depends on what provides LoadBalancer support
  (MetalLB, `minikube tunnel`, `cloud-provider-kind`); without any, the
  address stays `<pending>` and only `kubectl port-forward` works — in which
  case there is little point going past 6.1.
- **Only one Ingress controller running at a time**, while learning. If
  ingress-nginx from [`4.1_ingress_nginx`](../4.1_ingress_nginx/) is still
  installed, remove it first: two controllers watching the same Ingress
  objects makes for confusing results.

Replace `jeremiedecock` with your own GitHub username, here and in
`deployment.yml`:

```shell
sed -i 's/jeremiedecock/your-github-username/g' deployment.yml
```

## 1. Create a Personal Access Token

If 6.1 is still fresh, your token is already in `$GHCR_TOKEN` and you are
logged in — skip to step 2.

Otherwise, create a **PAT (classic)** as described in
[Authenticating with a personal access token](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-with-a-personal-access-token-classic),
with the scopes `read:packages`, `write:packages`, `delete:packages` and
`repo`. Only `read:packages` is needed by the cluster; the others are for you
(push, and cleanup). Keep it in your `.bashrc`:

```shell
export GHCR_TOKEN=ghp_...
```

And log in, token on stdin so that it stays out of your shell history:

```shell
echo $GHCR_TOKEN | podman login ghcr.io -u jeremiedecock --password-stdin
```

## 2. Build and push the image

Same image, same tag as 6.1 — see
[Pushing container images](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#pushing-container-images):

```shell
podman build -t ghcr.io/jeremiedecock/hello-fastapi:1.0 .
```

Optional, and the quickest way to rule the app out of any later problem:

```shell
podman run -p 8000:8000 ghcr.io/jeremiedecock/hello-fastapi:1.0
```

Open `http://localhost:8000` for the FastAPI welcome message, or
`http://localhost:8000/docs` for the generated documentation. `Ctrl+C` stops
it.

```shell
podman push ghcr.io/jeremiedecock/hello-fastapi:1.0
```

Check the pushed image at <https://github.com/jeremiedecock?tab=packages>.
It is **private**, which is why the next step exists.

## 3. Create the namespace and the pull Secret

```shell
kubectl create namespace snippet-backend-ingress-demo
```

Add `-n snippet-backend-ingress-demo` to every `kubectl` command below.

The Secret is detailed in
[6.1](../6.1_private_docker_registry/#4-create-the-pull-secret); in short, it
wraps the token in the `dockerconfigjson` format the kubelet expects, and
`deployment.yml` names it in `imagePullSecrets`:

```shell
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username='jeremiedecock' \
  --docker-password="$GHCR_TOKEN" \
  -n snippet-backend-ingress-demo
```

That `-n` is not optional: a pull Secret is a **namespaced** object, and the
kubelet only looks for it in the namespace of the Pod that references it. A
Secret in `default` is invisible to a Pod anywhere else — the single most
common cause of `ImagePullBackOff` in this chapter.

```shell
kubectl get secret ghcr-secret -n snippet-backend-ingress-demo
```

## 4. Install the Traefik controller

An Ingress object is only a *description*; a controller has to implement it.
[Traefik](https://doc.traefik.io/traefik/) is the one used here — still
maintained, and the default on k3s — installed with
[Helm](https://helm.sh/), as in
[`4.2_ingress_traefik`](../4.2_ingress_traefik/):

```shell
helm repo add traefik https://traefik.github.io/charts
helm repo update
helm install traefik traefik/traefik
```

Note that this installs Traefik in your *current* namespace (`default`,
normally), not in the demo namespace. The controller is cluster-wide
infrastructure serving every Ingress on the cluster, so it deliberately does
not live with the app.

**Check first whether Traefik is already there** — and in particular on k3s,
which ships it pre-installed in `kube-system`:

```shell
kubectl get svc -A -l app.kubernetes.io/name=traefik
kubectl get ingressclass
```

If it is, **skip the `helm install` and reuse it**. Running it anyway is not a
harmless no-op: `IngressClass` is a cluster-scoped object, so a second release
trying to create the class named `traefik` fails with an ownership error
("invalid ownership metadata"), and any release name that *does* succeed gives
you two controllers fighting over the same Ingress objects.

What matters is that the IngressClass name matches `ingressClassName` in
`ingress.yml`. That class is named after the **Helm release**, not the chart:
the command above creates a release called `traefik`, hence
`ingressClassName: traefik`. Install it under another name and the Ingress has
to be adjusted — otherwise no controller claims it, and it stays silently
unrouted with no error anywhere.

## 5. Deploy the app

```shell
kubectl apply -f deployment.yml -f service.yml -f ingress.yml \
  -n snippet-backend-ingress-demo
```

Then look at the whole app at once:

```shell
kubectl get all -n snippet-backend-ingress-demo
```

Two things to read in that output:

- `deployment.apps/my-deployment` at `READY 1/1`, and below it a
  `replicaset.apps/my-deployment-<hash>` — the intermediate object from
  [`3.1_replica_set`](../3.1_replica_set/), created by the Deployment, not by
  you;
- `service/my-service` with a `CLUSTER-IP` and no external address: that is
  what ClusterIP means. The public address belongs to Traefik, in its own
  namespace, which is why it does not appear here.

The Pods have to pull from GHCR and then pass the readiness probe, so give
them a few seconds:

```shell
kubectl rollout status deployment/my-deployment -n snippet-backend-ingress-demo
```

Before going outside, confirm the two internal hops the Ingress depends on.
The Service must have an endpoint — an empty list means either that no Pod is
ready, or that its `selector` does not match the Pods, and everything above it
will answer `503`:

```shell
kubectl get endpointslices -l kubernetes.io/service-name=my-service \
  -n snippet-backend-ingress-demo
```

(`kubectl get endpoints my-service` shows the same thing in a more compact
form, but the Endpoints API is deprecated in favour of EndpointSlice since
Kubernetes 1.33.)

And the Ingress must have been claimed by Traefik, i.e. show a populated
`ADDRESS` column:

```shell
kubectl get ingress my-ingress -n snippet-backend-ingress-demo
```

## 6. Test it

The Ingress's own `ADDRESS` is the address to use, and reading it from there
rather than from the Traefik Service works wherever the controller happens to
live:

```shell
ADDR=$(kubectl get ingress my-ingress -n snippet-backend-ingress-demo \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}{.status.loadBalancer.ingress[0].hostname}')
echo $ADDR
```

Both fields are asked for on purpose: cloud providers publish either an `ip`
(GCP, most on-prem LoadBalancers) or a `hostname` (AWS ELB), never both, so
concatenating them yields whichever exists. A `jsonpath` asking only for `.ip`
silently returns an empty string on AWS.

`ingress.yml` declares **no `host:`**, so this Ingress matches any hostname
and the bare address works. That is fine because there is only one app behind
this Traefik; the moment there are two, each needs its own `host:` — which is
what [`4.3.2`](../4.3.2_gateway_api_envoy_gateway_multi_apps/) and
[`5.4`](../5.4_lets_encrypt_multi_apps/) are about.

```shell
curl http://$ADDR/
```

```json
{"message":"hello"}
```

And the part that makes a FastAPI backend pleasant to demo — the interactive
documentation it generates from the code, served from the same Ingress:

```shell
curl http://$ADDR/openapi.json
```

Open `http://<ADDRESS>/docs` in a browser for the Swagger UI.

Optionally, create a DNS `A` record pointing at that address, and use the name
instead. Nothing in the manifests has to change (again: no `host:`), and it is
the prerequisite for getting a real certificate later.

**About `https://`.** Nothing in this directory configures TLS, so there is no
certificate of yours anywhere. The Traefik chart does expose a `websecure`
entrypoint on 443, and an Ingress with no `tls:` section is usually served
there too, with Traefik's **own default self-signed certificate** — so
depending on your chart version and values, `https://<ADDRESS>/docs` either
answers with a browser warning or does not answer at all. Both are expected;
neither is HTTPS worth the name:

```shell
curl -k https://$ADDR/docs
```

Encrypted, trusted by nobody — the situation of [`5.1_tls`](../5.1_tls/). Real
certificates are [`5.2_lets_encrypt`](../5.2_lets_encrypt/)'s job, and
[`6.3`](../6.3_stateless_backend_gateway_api_envoy_gateway_with_lets_encrypt/)
is where this app gets one.

## What the Deployment buys you

Worth two minutes, since 6.1's bare Pod could do none of it.

**Scale it**, and watch the Service spread traffic over the replicas:

```shell
kubectl scale deployment/my-deployment --replicas=3 -n snippet-backend-ingress-demo
kubectl get pods -o wide -n snippet-backend-ingress-demo
```

Then hit the app a few times and look at which Pod answered — each has its own
access log:

```shell
for i in $(seq 6); do curl -s http://$ADDR/ > /dev/null; done
kubectl logs -l app=my-app --prefix --tail=3 -n snippet-backend-ingress-demo
```

`-l app=my-app` selects by label rather than by name, which is how you read
logs from a set of Pods whose names you do not know.

**Update it.** Rebuild under a new tag and roll it out — without touching the
Service or the Ingress:

```shell
podman build -t ghcr.io/jeremiedecock/hello-fastapi:1.0.1 .
podman push ghcr.io/jeremiedecock/hello-fastapi:1.0.1
kubectl set image deployment/my-deployment \
  my-container=ghcr.io/jeremiedecock/hello-fastapi:1.0.1 \
  -n snippet-backend-ingress-demo
kubectl rollout status deployment/my-deployment -n snippet-backend-ingress-demo
```

`my-container=` is the **container** name from `deployment.yml`, not the
Deployment's. A new tag rather than a rebuilt `1.0` is the point of the
exercise: same code here, but had you changed `main.py`, overwriting `1.0`
would leave every other demo in the series pulling something they did not
expect.

And if the new version is broken:

```shell
kubectl rollout undo deployment/my-deployment -n snippet-backend-ingress-demo
```

Scale back down before moving on, if you scaled up:

```shell
kubectl scale deployment/my-deployment --replicas=1 -n snippet-backend-ingress-demo
```

## When it does not work

Work from the outside in: Ingress, then Service, then Pods. Each layer has a
characteristic failure.

- **`404 page not found` from Traefik.** The request reached the controller
  and matched no route. Either the Ingress was never claimed (its `ADDRESS`
  is empty — check `ingressClassName` against `kubectl get ingressclass`,
  remembering the release-name rule), or you are querying a hostname the rule
  does not cover. `kubectl describe ingress my-ingress` and the controller's
  own log are the two places to look — with the namespace Traefik actually
  runs in, `kube-system` on k3s:
  `kubectl logs -l app.kubernetes.io/name=traefik -A --tail=20`.
- **`503 Service Unavailable`.** Routing worked, there is nothing to route
  *to*. Almost always no ready endpoint behind the Service: the
  `endpointslices` command above comes back empty because the Pods are not
  ready, or because `service.yml`'s `selector` (`app: my-app`) does not match
  `deployment.yml`'s labels. Sometimes it is the port instead: the Ingress
  names a port the Service does not expose (`80` here, not `8000`).
- **Pods in `ImagePullBackOff` / `ErrImagePull`.** The registry side, as in
  6.1: `kubectl describe pod -l app=my-app | tail -20` has the registry's own
  answer. `401` means the Secret is missing, misnamed in `imagePullSecrets`,
  **in another namespace**, or built with a `--docker-server` other than
  exactly `ghcr.io`.
- **Pods `Running` but `0/1 READY`.** The readiness probe is failing.
  `kubectl describe pod -l app=my-app` spells out the status code it got.
  With this app it means the container is up but not serving — check
  `kubectl logs`.
- **Pods `CrashLoopBackOff`.** Not a Kubernetes problem:
  `kubectl logs -l app=my-app` is the app's own traceback. An app bound to
  `127.0.0.1` instead of `0.0.0.0` is the classic one — it starts fine and is
  unreachable from anywhere.
- **No `ADDRESS` on the Ingress, and `<pending>` on the Traefik Service.**
  Your cluster has no LoadBalancer provider (see *Prerequisites*). Fall back
  to `kubectl port-forward svc/my-service 8080:80 -n snippet-backend-ingress-demo`
  to at least reach the app, but the Ingress part of this example cannot be
  demonstrated.

## Remove the demo

```shell
kubectl delete -f deployment.yml -f service.yml -f ingress.yml \
  -n snippet-backend-ingress-demo
kubectl delete namespace snippet-backend-ingress-demo
```

Deleting the namespace takes the `ghcr-secret` Secret with it — which is the
other benefit of not having put it in `default`.

This leaves the **Traefik controller** in place; it is cluster-wide
infrastructure, shared by every Ingress. Remove it only if you installed it
for this example and nothing else uses it:

```shell
kubectl get ingress --all-namespaces
helm uninstall traefik
```

**Keep the image.** `hello-fastapi:1.0` is this app — `{"message": "hello"}`,
documentation enabled — and 6.2.2 and 6.4 expect exactly that content behind
the tag. The later examples add their own tags rather than overwriting it
(`1.0.1` for the rolling update in this example, `4.0` and `5.0` for the
persistence chapters), so nothing in the series will change what `1.0` means
under you.

When you are done with the series, revoke the PAT from *Settings → Developer
settings → Personal access tokens* and clear the local credentials with
`podman logout ghcr.io`.
