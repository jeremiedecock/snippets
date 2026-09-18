# Two fullstack apps, two domains, one Gateway (Gateway API + Let's Encrypt)

This example is the meeting point of two earlier ones, and assumes both have
been read:

- [`6.4_stateless_fullstack_app`](../6.4_stateless_fullstack_app/) — **one**
  fullstack application: an nginx frontend and a FastAPI backend behind a
  single hostname, split by path (`/api` and `/`) in a single HTTPRoute,
  over HTTPS;
- [`5.4_lets_encrypt_multi_apps`](../5.4_lets_encrypt_multi_apps/) — **two**
  applications, each in its own namespace, sharing one Gateway, routed by
  hostname, each with its own Let's Encrypt certificate.

Here, **two fullstack applications are served over HTTPS under two different
domain names, behind a single public IP address**, each in its own namespace,
each with its own certificate, and each splitting its own hostname between a
frontend and a backend:

```
https://app1.example.com/       -> app1's page   (nginx,   namespace ...-app1)
https://app1.example.com/api/   -> {"message": "hello"}  (FastAPI, namespace ...-app1)

https://app2.example.com/       -> app2's page   (nginx,   namespace ...-app2)
https://app2.example.com/api/   -> {"message": "hello"}  (FastAPI, namespace ...-app2)
```

Nothing conceptual is new: the path split, the `URLRewrite` filter and
`--root-path` are explained in 6.4; the four listeners, the two certificates
and the cross-namespace route attachment in 5.4. This README does not repeat
either. It covers **what changes when the two are combined** — which is
mostly a question of *where the boundaries are drawn*: what is shared between
the two applications, what is duplicated, and why.

## What changes

| | `6.4` | `5.4` | `6.5` (here) |
| --- | --- | --- | --- |
| Applications | 1 | 2 | 2 |
| Components per application | **2** (front + back) | 1 | **2** (front + back) |
| Deployments / Services | 2 / 2 | 2 / 2 | **4 / 4** |
| Namespaces | 1, on the command line | 3, hardcoded | **3, hardcoded** |
| Images | 2 | 0 (stock nginx) | 2 — **shared by both apps** |
| Pull Secrets | 1 | none | **2**, one per app namespace |
| Hostnames | 1 | 2 | 2 |
| Listeners | 2 | 4 | 4 |
| Certificates | 1 | 2 | 2 |
| ClusterIssuers | 2 | 2 | 2, **unchanged** |
| HTTPRoutes | 2 | 4 | 4 (one app route + one redirect per application) |
| Rules in each app route | 2, matched on path | 1 | **2, matched on path** |
| `sectionName` on routes | recommended | **mandatory** | **mandatory** |
| DNS records | 1 `A` | 2 `A`, same IP | 2 `A`, **same IP** |

Two things are worth reading off that table. Going from 6.4 to 6.5 **doubles
the applications but adds no image and no cluster add-on**: the second
application is manifests only. And the column that does *not* grow is the
interesting one — one Gateway, one public IP, one pair of issuers, whatever
the number of applications behind them.

## Layout

One directory per namespace, every manifest hardcoding its
`metadata.namespace`, exactly as in 5.4 — with 6.4's `backend/` and
`frontend/` split nested inside each application:

```
images/                           # build contexts, once for both applications
├── backend/
│   ├── main.py                   #   three lines of FastAPI: GET / -> {"message": "hello"}
│   └── Containerfile             #   -> ghcr.io/<you>/hello-fastapi:1.0   (built in 6.1)
└── frontend/
    ├── index.html                #   one static page, which fetches /api/ and displays it
    └── Containerfile             #   -> ghcr.io/<you>/hello-frontend:1.0  (built in 6.4)

gateway-class/gateway-class.yml   # cluster-wide, belongs to no namespace
gateway/                          # namespace snippet-fullstack-multi-demo-gateway
├── namespace.yml
├── cluster-issuer.yml            # cluster-wide too (see below)
└── gateway.yml                   # 4 listeners: http/https x app1/app2

app1/                             # namespace snippet-fullstack-multi-demo-app1
├── namespace.yml
├── secret.yml                    # the pull Secret, for reference only
├── backend/
│   ├── deployment.yml            #   + --root-path /api
│   └── service.yml
├── frontend/
│   ├── deployment.yml
│   └── service.yml
├── http-route.yml                # >>> /api -> backend, / -> frontend, on https-app1
└── http-redirect-route.yml       # 301 http -> https, on http-app1

app2/                             # namespace snippet-fullstack-multi-demo-app2
└── ... identical, with app1 replaced by app2 throughout
```

The `images/` directory is the one departure from both parents, and it says
something: **the build contexts appear once, not per application**, because
both applications run the same two images. The multiplicity of this example
is in the routing and in the namespaces, not in the code — as in 5.4, where
the two applications were deliberately the same stock nginx so that the only
variable on display was the certificate handling.

| Hostname | Namespace | Listeners | Certificate / Secret | Services |
| --- | --- | --- | --- | --- |
| `app1.example.com` | `snippet-fullstack-multi-demo-app1` | `http-app1`, `https-app1` | `app1-tls` | `frontend`, `backend` |
| `app2.example.com` | `snippet-fullstack-multi-demo-app2` | `http-app2`, `https-app2` | `app2-tls` | `frontend`, `backend` |

`cluster-issuer.yml` sits in `gateway/` because its HTTP-01 solver names this
demo's Gateway, but the two ClusterIssuers it declares are **cluster-scoped**:
like the GatewayClass, they survive the deletion of the namespace and have to
be removed explicitly.

## The chain

```
                                          app1.example.com
                                  +--> /api/* --[strip /api]--> Service backend  --> Pod (FastAPI :8000)
                                  |                                  namespace ...-app1
                       [SNI app1] +--> /*     ----------------> Service frontend --> Pod (nginx :80)
                          ^       |
browser --HTTPS--> Gateway (Envoy)
                          v       |          app2.example.com
                       [SNI app2] +--> /api/* --[strip /api]--> Service backend  --> Pod (FastAPI :8000)
                                  |                                  namespace ...-app2
                                  +--> /*     ----------------> Service frontend --> Pod (nginx :80)

               one public IP, one Gateway
               two certificates, chosen by SNI
               two HTTPRoutes, each one splitting its own hostname by path
```

Two decisions, taken in this order and by two different mechanisms:

1. **which application** — by hostname. On port 443 that happens during the
   TLS handshake, through SNI, *before* any HTTP byte is exchanged: the
   client announces the name it wants, Envoy picks the matching listener and
   presents that listener's certificate. This is 5.4.
2. **which half of that application** — by path, once the request is decrypted
   and its `Host` header has selected the route. This is 6.4.

Nothing in step 2 can reach across into the other application: the two
HTTPRoutes are attached to two different listeners, live in two different
namespaces, and forward to Services in their own namespace only.

## Two applications, two origins

6.4's point was that one hostname makes `fetch("/api/")` a **same-origin**
request, so CORS never enters the picture. That property is per application
and it survives untouched here: `app1.example.com` serves both app1's page
and app1's API, so app1's JavaScript reads app1's JSON without a single
`Access-Control-Allow-Origin` header anywhere.

What is new is what happens *between* the two applications: they are mutually
**cross-origin**. A page served from `app1.example.com` that tried to
`fetch("https://app2.example.com/api/")` would get the full CORS treatment —
an `Origin` header, a preflight for anything non-trivial, and a response the
browser refuses to hand over unless app2 opted in.

That is the correct outcome, not a limitation. The browser's origin boundary
now lines up with the namespace boundary and with the team boundary: one
hostname, one namespace, one set of routes, one certificate, one origin. Two
applications that genuinely need to call each other should do so
**server-side**, where the same-origin policy does not apply at all — Pod to
Service, over cluster-internal DNS, without ever leaving the cluster.

## One namespace per application, both halves inside it

4.3.2 and 5.4 put each application in its own namespace. The question this
example raises, and that they could not, is: with *two components* per
application, where does the namespace boundary go?

| Split | Namespaces here | |
| --- | --- | --- |
| **per application** (used here) | 2 | frontend and backend of one app together |
| per component | 4 | `app1-frontend`, `app1-backend`, `app2-frontend`, … |
| per environment | 2 | `prod`, `staging`, everything inside |

Per application is the right default, and the reasons are concrete rather
than aesthetic:

- a frontend and the backend it is published with are **deployed together,
  released together and owned by one team**. A namespace is the unit that
  ResourceQuotas, LimitRanges, RBAC and NetworkPolicies apply to, so it
  should match the unit of ownership;
- an HTTPRoute's `backendRefs` may target **any Service in its own
  namespace** with no further ceremony. Split the two halves across two
  namespaces and the route needs a cross-namespace `backendRef`, which the
  Gateway API refuses unless the target namespace publishes a
  **`ReferenceGrant`** accepting it. That is a useful safeguard between
  teams, and pure overhead inside one application;
- the pull Secret, the ConfigMaps and the NetworkPolicies of one application
  stay in one place.

Note the asymmetry, because it is the rule worth remembering: **attaching a
route to a Gateway in another namespace needs no ReferenceGrant** — it is
governed by `allowedRoutes` on the listener, i.e. by the cluster operator —
while **forwarding to a Service in another namespace does**, and is governed
by the owner of that Service. Permission is always granted by the side being
pointed at.

## What is shared, and what is not

| | Shared | Per application |
| --- | --- | --- |
| Public IP, Gateway, GatewayClass | ✅ one | |
| ClusterIssuers, ACME account | ✅ one pair | |
| cert-manager, Envoy Gateway controller | ✅ cluster add-ons | |
| Container images (`hello-fastapi:1.0`, `hello-frontend:1.0`) | ✅ same tags | |
| Listeners | | 2 (HTTP + HTTPS) |
| Certificate / TLS Secret | | 1, in the **Gateway's** namespace |
| Namespace, Deployments, Services | | 1 / 2 / 2 |
| HTTPRoutes | | 2 (app route + redirect) |
| Registry pull Secret | | **1 — same contents, different namespace** |
| DNS `A` record | | 1, same IP |

The last line of the middle column and the last of the right-hand one are the
two that catch people out, and they are the next two sections.

## The pull Secret, once per namespace

A pull Secret is a **namespaced** object, and the kubelet only looks for it
in the namespace of the Pod that references it. There is no such thing as
sharing one across namespaces, so each application namespace gets its own
copy, with identical contents:

```shell
kubectl create secret docker-registry ghcr-secret ... -n snippet-fullstack-multi-demo-app1
kubectl create secret docker-registry ghcr-secret ... -n snippet-fullstack-multi-demo-app2
```

Within one namespace, though, it stays **one Secret for both images**: the
credentials belong to the *registry*, not to a repository. Four Pods, two
images, two Secrets — one per namespace.

This duplication is the visible tip of a real operational problem: a cluster
with fifty namespaces pulling from one private registry ends up with fifty
copies of one credential to rotate together. The usual answers are a Secret
replicator (`reflector`, `kubed`) which copies an annotated Secret into
matching namespaces, a
[credential provider](https://kubernetes.io/docs/tasks/administer-cluster/kubelet-credential-provider/)
configured on the nodes so no Secret is needed at all, or — on a managed
cluster — making the node identity itself entitled to pull. Two copies do not
justify any of that; twenty do.

## Same names, different namespaces

Both applications name their Services `frontend` and `backend`, both label
their Pods `app: frontend` / `app: backend`, and both call their routes
`my-route` and `my-redirect-route`. None of it collides, and none of it is
accidental: a namespace is exactly the scope within which a name must be
unique. A Service's `selector` only ever matches Pods in its own namespace,
and an HTTPRoute's `backendRefs` resolve in its own namespace by default.

The consequence to keep in mind is that **every `kubectl` command below needs
its `-n`**, and that a command run against the wrong namespace will happily
succeed on the wrong object. It also shows up in the cluster-internal DNS
name, which is where the namespace reappears:

```
backend.snippet-fullstack-multi-demo-app1.svc.cluster.local
backend.snippet-fullstack-multi-demo-app2.svc.cluster.local
```

From inside one of the two namespaces, plain `backend` resolves to the local
one — which is what makes the *same* manifest, and the same image, work in
both.

## The Gateway: four listeners

Unchanged from 5.4, and it does not know that anything behind it became
fullstack:

```yaml
listeners:
  - name: http-app1     # HTTP  :80   hostname app1.example.com
  - name: https-app1    # HTTPS :443  hostname app1.example.com  -> Secret app1-tls
  - name: http-app2     # HTTP  :80   hostname app2.example.com
  - name: https-app2    # HTTPS :443  hostname app2.example.com  -> Secret app2-tls
```

Several listeners may share a port, provided their `hostname` values differ
and their `name` values are unique. On 443 Envoy picks the certificate by
**SNI**, on 80 the route by the `Host` header.

Two consequences for the routes, both inherited from 5.4:

- `sectionName` is **mandatory** in every `parentRefs`. With four listeners,
  omitting it attaches the route to every listener whose hostname is
  compatible — including the HTTP one, which would defeat the redirect;
- each application owns **two** HTTPRoutes: the real one on its HTTPS
  listener, and the 301 redirect on its HTTP listener. Both live in the
  application's namespace, next to what they expose.

And one inherited from 6.4: the *real* route carries **two rules**, matched
on path. The Gateway sees one route on one hostname and never learns that it
fans out to two Services — which is the whole division of labour the Gateway
API is built around. Adding a third component to app1 (an admin UI under
`/admin`, say) changes `app1/http-route.yml` and nothing else: no listener,
no certificate, no DNS record, and nothing in app2.

> **On the HTTP listeners.** A single listener on port 80 with *no* hostname
> would serve both applications' redirects and both ACME challenges just as
> well, and cert-manager would ignore it either way — it only looks at HTTPS
> listeners. Four listeners are used here because the symmetry makes the
> ownership obvious: everything about `app1.example.com` is named after it.

## The ACME challenge, twice

Exactly 5.4's, and worth re-reading there. The two challenges run **in
parallel and independently**: two `Certificate`s, two `Order`s, two
`Challenge`s and two sets of temporary solver objects (Pod, Service and
HTTPRoute) — all of them in the **Gateway's** namespace, since that is where
the Certificates are. The gateway-shim does not support cross-namespace
`certificateRefs`, so an application team never sees the private key of the
certificate that fronts it.

The one trap, again: the issuer's
`solvers[].http01.gatewayHTTPRoute.parentRefs` **must not carry a
`sectionName`**. That single parentRef is reused for every challenge of every
domain, so pinning it to one listener would send the `app2` challenge to a
listener whose hostname is `app1.example.com`; the hostnames would not
intersect, the solver route would not attach, and the challenge would time
out with a 404.

A second trap is specific to this example, and 6.4 warns about it too: each
application's catch-all `/` rule sends everything it matches to nginx,
including — one might fear — the challenge path. It does not. The solver
route matches `/.well-known/acme-challenge/<token>` **exactly**, an Exact
match outranks any prefix, and the ranking applies across routes. If a
challenge ever returns nginx's index page, the solver route is not there at
all: look at the cert-manager logs, not at `http-route.yml`.

## Prerequisites

Exactly 6.4's, with one DNS record per application:

- a **container engine** (Podman or Docker) and a **GitHub account**, for the
  two images — see 6.1;
- **Envoy Gateway and the `eg` GatewayClass** — see
  [4.3.1](../4.3.1_gateway_api_envoy_gateway/README.md#prerequisite-a-gateway-api-implementation),
  including the checks to make before installing anything cluster-wide;
- **cert-manager, with its Gateway API integration enabled** — see
  [5.2](../5.2_lets_encrypt/README.md#installing-cert-manager). The
  `config.gatewayAPI.enabled=true` setting is the one that is off by default
  and silently does nothing when forgotten;
- **a cluster whose Gateway gets a public IP**, reachable from the internet on
  ports 80 and 443. Let's Encrypt validates the domains from the internet, so
  minikube and kind cannot be used here, and `curl --resolve` or `/etc/hosts`
  tricks do not help: the ACME server resolves the names itself;
- **two domain names you own**, pointing at that address (created a few steps
  below, once the address exists).

Replace the example domains with your own, the GitHub username with yours, and
the contact address in the issuers:

```shell
sed -i 's/app1\.example\.com/app1.your-domain.com/g' gateway/gateway.yml app1/*.yml
sed -i 's/app2\.example\.com/app2.your-domain.com/g' gateway/gateway.yml app2/*.yml
sed -i 's/you@example\.com/your-address@your-domain.com/g' gateway/cluster-issuer.yml
sed -i 's/jeremiedecock/your-github-username/g' app1/*/deployment.yml app2/*/deployment.yml app1/secret.yml app2/secret.yml
```

## 1. Build and push the two images

**If 6.4 has been done and both images are still on GHCR, skip this step
entirely** — this example runs those exact tags, and runs them twice.

Otherwise, log in (create a **PAT (classic)** with `read:packages`,
`write:packages`, `delete:packages` and `repo` first, as described in 6.1):

```shell
export GHCR_TOKEN=ghp_...
echo $GHCR_TOKEN | podman login ghcr.io -u jeremiedecock --password-stdin
```

```shell
podman build -t ghcr.io/jeremiedecock/hello-fastapi:1.0  images/backend/
podman push  ghcr.io/jeremiedecock/hello-fastapi:1.0

podman build -t ghcr.io/jeremiedecock/hello-frontend:1.0 images/frontend/
podman push  ghcr.io/jeremiedecock/hello-frontend:1.0
```

(With `docker`, add `-f images/backend/Containerfile` / `-f
images/frontend/Containerfile`: Docker looks for a file named `Dockerfile` by
default.)

Both packages are **private** by default at
<https://github.com/jeremiedecock?tab=packages>, hence the pull Secrets in
step 4.

## 2. Install Envoy Gateway and the GatewayClass

Both the Gateway API CRDs and their controller are **cluster-wide and
shared**, so check before installing anything. Empty output or a `NotFound`
means absent:

```shell
kubectl api-resources --api-group=gateway.networking.k8s.io
kubectl get deployments -n envoy-gateway-system
helm list --all-namespaces
```

If they are already there, skip the `helm install` and go straight to the
GatewayClass check. Otherwise:

```shell
helm install eg oci://docker.io/envoyproxy/gateway-helm --version v1.9.1 -n envoy-gateway-system --create-namespace
kubectl wait --timeout=5m -n envoy-gateway-system deployment/envoy-gateway --for=condition=Available
```

Then the GatewayClass, cluster-wide too:

```shell
kubectl get gatewayclass
```

If an entry already has `gateway.envoyproxy.io/gatewayclass-controller` in
its `CONTROLLER` column, reuse it: put its name in `spec.gatewayClassName` of
`gateway/gateway.yml` and skip the apply. Otherwise:

```shell
kubectl apply -f gateway-class/gateway-class.yml
kubectl get gatewayclass
```

`ACCEPTED` must read `True` — `False` or `Unknown` means the controller is
not running.

## 3. Install cert-manager

Another cluster-wide add-on, so again, look first:

```shell
kubectl get deployments -n cert-manager
kubectl api-resources --api-group=cert-manager.io
```

If it is already installed, skip to the integration check below — the
integration still has to be enabled, and it is off by default. Otherwise:

```shell
helm install cert-manager oci://quay.io/jetstack/charts/cert-manager \
  --version v1.21.2 \
  --namespace cert-manager --create-namespace \
  --set crds.enabled=true \
  --set config.gatewayAPI.enabled=true
```

```shell
kubectl wait --timeout=5m -n cert-manager deployment --all --for=condition=Available
```

cert-manager checks for the Gateway API CRDs **only at startup**, so restart
it if it was installed before Envoy Gateway. The second command should print
`true`:

```shell
kubectl rollout restart deployment cert-manager -n cert-manager
kubectl get configmap cert-manager -n cert-manager -o yaml | grep -A2 gatewayAPI
```

**Without it, the annotation in `gateway/gateway.yml` is ignored and nothing
happens** — no Certificate, no error, no event.

## 4. Deploy the Gateway

The Gateway namespace, the issuers and the Gateway. The issuers are applied
before the Gateway so that the two Certificates the annotation triggers find
their `issuerRef` right away:

```shell
kubectl apply \
  -f gateway/namespace.yml \
  -f gateway/cluster-issuer.yml \
  -f gateway/gateway.yml
```

```shell
kubectl get clusterissuer
```

Two ClusterIssuers, `letsencrypt-staging` and `letsencrypt`, differing only
by the ACME server URL, both naming this demo's Gateway in their HTTP-01
solver, and both serving **the two applications at once**. Always start with
staging, which `gateway/gateway.yml` does.

Wait for the Gateway's `ADDRESS` column to be populated (`Ctrl+C` to stop
watching). `PROGRAMMED` stays `False`, as in 5.4 — now because *two*
listeners point at Secrets that do not exist yet:

```shell
kubectl get gateway -n snippet-fullstack-multi-demo-gateway --watch
```

`describe` reports the state listener by listener, which is the view that
matters from here on — `http-app1` and `http-app2` are already serving, while
the two HTTPS ones are unresolved:

```shell
kubectl describe gateway my-gateway -n snippet-fullstack-multi-demo-gateway
```

### Point both domains at the Gateway

```shell
GATEWAY_IP=$(kubectl get gateway my-gateway -n snippet-fullstack-multi-demo-gateway -o jsonpath='{.status.addresses[0].value}')
echo $GATEWAY_IP
```

Create **two** `A` records, `app1` and `app2`, both pointing at that same
address (or two `CNAME`s if your provider hands out a hostname), then check
that both resolve before going further — a stale record is the single most
common cause of a failing challenge:

```shell
dig +short app1.example.com
dig +short app2.example.com
```

## 5. Deploy the two applications

The namespaces first, because the pull Secrets go into them:

```shell
kubectl apply -f app1/namespace.yml -f app2/namespace.yml
```

Then one pull Secret per namespace, with the same credentials. The `-n` is
not optional: the kubelet only looks for the Secret in the namespace of the
Pod that references it.

```shell
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username='jeremiedecock' \
  --docker-password="$GHCR_TOKEN" \
  -n snippet-fullstack-multi-demo-app1

kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username='jeremiedecock' \
  --docker-password="$GHCR_TOKEN" \
  -n snippet-fullstack-multi-demo-app2
```

```shell
kubectl get secret ghcr-secret -n snippet-fullstack-multi-demo-app1
kubectl get secret ghcr-secret -n snippet-fullstack-multi-demo-app2
```

Then everything else. Each manifest carries its own namespace, so no `-n` is
needed on the applies:

```shell
kubectl apply \
  -f app1/backend/deployment.yml \
  -f app1/backend/service.yml \
  -f app1/frontend/deployment.yml \
  -f app1/frontend/service.yml \
  -f app1/http-route.yml \
  -f app1/http-redirect-route.yml
```

```shell
kubectl apply \
  -f app2/backend/deployment.yml \
  -f app2/backend/service.yml \
  -f app2/frontend/deployment.yml \
  -f app2/frontend/service.yml \
  -f app2/http-route.yml \
  -f app2/http-redirect-route.yml
```

> **Do not use `kubectl apply -R -f app1/` here**, convenient as it looks —
> `-R` reads the directory recursively and would pick up `secret.yml`, whose
> placeholder password (`ghp_...`) would overwrite the Secret created just
> above and break the image pull. That file is a reference, not an input. If
> you did apply it, recreate the Secret with the `kubectl create secret`
> command again, adding `--dry-run=client -o yaml | kubectl apply -f -`.

Wait for the four Deployments:

```shell
for ns in app1 app2; do
  kubectl rollout status deployment/backend  -n snippet-fullstack-multi-demo-$ns
  kubectl rollout status deployment/frontend -n snippet-fullstack-multi-demo-$ns
done
```

Check that the four routes were accepted, and that each landed on the
listener it asked for — a wrong or missing `sectionName` shows up here, and
so does a typo in either `backendRefs`:

```shell
kubectl describe httproute -n snippet-fullstack-multi-demo-app1
kubectl describe httproute -n snippet-fullstack-multi-demo-app2
```

Look for `Accepted: True` and `ResolvedRefs: True` under `Parents`. With two
`backendRefs` per route, `ResolvedRefs` covers both: a typo in either Service
name turns it `False`, and the *other* rule keeps working — which is exactly
the half-broken state to expect when only one half of one application
misbehaves.

Both redirects should already answer on port 80, before any certificate
exists:

```shell
curl -I http://app1.example.com/
curl -I http://app2.example.com/
```

## 6. Watch the two certificates being issued

Everything happens in the Gateway's namespace. Two Certificates appear, named
after the Secrets of the two HTTPS listeners, and go `READY=True` a minute or
two after DNS resolves correctly:

```shell
kubectl get certificate -n snippet-fullstack-multi-demo-gateway --watch
```

Nobody wrote those objects: cert-manager's gateway-shim generated them from
the two annotated listeners. The whole chain, doubled — two Orders, two
Challenges, running at the same time:

```shell
kubectl get certificate,certificaterequest,order,challenge -n snippet-fullstack-multi-demo-gateway
kubectl describe challenge -n snippet-fullstack-multi-demo-gateway
```

`kubectl describe challenge` is the single most useful command when this
hangs: its status message is the verbatim answer Let's Encrypt got when it
fetched the token.

The two are genuinely independent: if only one hostname is wrong, one
Certificate goes `READY=True` and the other keeps retrying. The Gateway as a
whole stays `PROGRAMMED=False` until both are there, but the working hostname
is served over HTTPS in the meantime.

Once both are ready, the cluster holds **four Secrets of two different
kinds**: two `ghcr-secret` you created to *pull* the images, in the
application namespaces, and two TLS Secrets cert-manager created to *serve*
them, in the Gateway's:

```shell
kubectl get secret app1-tls app2-tls -n snippet-fullstack-multi-demo-gateway
kubectl get gateway -n snippet-fullstack-multi-demo-gateway
```

Read the two certificates back, and check that each carries its own single
name — the `Subject` line is the interesting one:

```shell
for name in app1 app2; do
  kubectl get secret $name-tls -n snippet-fullstack-multi-demo-gateway \
    -o jsonpath='{.data.tls\.crt}' | base64 -d \
    | openssl x509 -noout -subject -issuer -dates
done
```

The issuer reads `(STAGING)` something, from Let's Encrypt's test hierarchy.

## 7. Test all four halves, with the staging certificates

`curl` refuses the staging certificates, as every client does — `-k` skips
the check and confirms that everything but the trust chain works. Four
requests, two hostnames, two paths each:

```shell
curl -k https://app1.example.com/api/          # {"message":"hello"}
curl -ks https://app1.example.com/ | head -3   # <!DOCTYPE html> ...

curl -k https://app2.example.com/api/          # {"message":"hello"}
curl -ks https://app2.example.com/ | head -3   # <!DOCTYPE html> ...
```

The rewrite is easiest to see on a path that exists on neither side — compare
who answers, and in which language:

```shell
curl -k https://app1.example.com/api/nope   # FastAPI:  {"detail":"Not Found"}
curl -k https://app1.example.com/nope       # nginx:    <html>404 Not Found</html>
```

And the documentation, which is the reason `--root-path` is in each
`backend/deployment.yml` — note the `servers` entry in the schema, which is
the app telling clients where it really lives:

```shell
curl -k https://app1.example.com/api/openapi.json | head -c 200
```

The answers are identical on both hostnames, because both applications run
the same two images. The check that actually proves they are *two*
applications is the one 5.4 made — a different certificate per name, selected
by SNI on the same IP and the same port:

```shell
for name in app1 app2; do
  openssl s_client -connect $name.example.com:443 -servername $name.example.com </dev/null 2>/dev/null \
    | openssl x509 -noout -subject
done
```

Both commands open a connection to the same IP and the same port; the only
difference is the name announced by the client before the handshake, and that
is all SNI is.

And the second proof, which is this example's own: the request lands in a
*different namespace* depending on the hostname. Watch it in the logs —
call app1 only, and only app1's backend Pod logs a line:

```shell
curl -ks https://app1.example.com/api/ > /dev/null
kubectl logs -l app=backend --tail=3 -n snippet-fullstack-multi-demo-app1
kubectl logs -l app=backend --tail=3 -n snippet-fullstack-multi-demo-app2
```

Note the path in those lines — `"GET / HTTP/1.1"`, not `/api/`: what the
application sees is what the `URLRewrite` filter left of the request.

## 8. Switch to the production issuer

Only once the above works end to end for **both** hostnames. Changing the one
annotation re-issues **both** certificates:

```shell
sed -i 's|cert-manager.io/cluster-issuer: letsencrypt-staging|cert-manager.io/cluster-issuer: letsencrypt|' gateway/gateway.yml
kubectl apply -f gateway/gateway.yml
```

```shell
kubectl get certificate -n snippet-fullstack-multi-demo-gateway --watch
```

Then plain `curl`, with no flag at all, on both:

```shell
curl https://app1.example.com/api/
curl https://app2.example.com/api/
```

## 9. Open both in a browser

The step the whole series was heading towards, and the only one that cannot
be done with `curl`, because the point is what the *browser* does:

**<https://app1.example.com/>** and **<https://app2.example.com/>**

A padlock on each, no warning, and a page that says `hello` — a word that is
not in the HTML. Open the developer tools, *Network* tab, and reload:

- two requests, `/` and `/api/`, both to the hostname in the address bar,
  both `200`;
- **no `OPTIONS` preflight** before the second one, and no `Origin` header on
  it — the browser did not consider it a cross-origin request;
- no `Access-Control-Allow-Origin` in the answer, because none was needed.

That absence is the deliverable, and it is now true twice over, on two
origins that know nothing about each other.

`https://app1.example.com/api/docs` gives the Swagger UI of app1's backend,
under app1's padlock — and the schema loads, which it would not have done
without `--root-path`.

The two pages are byte-identical, since they come from one image. The URL bar
is what tells them apart, and that is the honest summary of this example:
**what makes two applications two applications is the hostname, the namespace
and the certificate — not the code.**

## Scaling and updating one application

Each half of each application scales on its own, and neither the Gateway, the
routes nor the certificates are touched by any of it:

```shell
kubectl scale deployment/backend --replicas=3 -n snippet-fullstack-multi-demo-app1
for i in $(seq 6); do curl -s https://app1.example.com/api/ > /dev/null; done
kubectl logs -l app=backend --prefix --tail=3 -n snippet-fullstack-multi-demo-app1
```

The log lines are spread across app1's three Pods, and app2 is untouched
throughout — different namespace, different Service, different
EndpointSlices.

Updating one application leaves the other running, and this is where sharing
an image tag between two applications stops being free:

```shell
podman build -t ghcr.io/jeremiedecock/hello-frontend:1.0.1 images/frontend/
podman push ghcr.io/jeremiedecock/hello-frontend:1.0.1
kubectl set image deployment/frontend \
  frontend=ghcr.io/jeremiedecock/hello-frontend:1.0.1 \
  -n snippet-fullstack-multi-demo-app1
kubectl rollout status deployment/frontend -n snippet-fullstack-multi-demo-app1
```

`frontend=` is the **container** name from the Deployment, and the new tag
matters twice as much here as in 6.4: overwriting `1.0` in place would change
what *both* applications pull on their next restart — a rollout of app1
silently rolling out app2 hours later, which is the classic argument for
immutable tags. `kubectl rollout undo deployment/frontend -n ...` reverts.
Scale back down before moving on:

```shell
kubectl scale deployment/backend --replicas=1 -n snippet-fullstack-multi-demo-app1
```

## When it does not work

6.4's three chains all apply, with one addition that covers most of what goes
wrong here: **look per application, and in the right namespace**. The
Certificates, Orders, Challenges and solver Pods are in
`snippet-fullstack-multi-demo-gateway`; the Deployments, Services and
HTTPRoutes in the two application namespaces.

```shell
kubectl describe gateway my-gateway -n snippet-fullstack-multi-demo-gateway
kubectl describe certificate -n snippet-fullstack-multi-demo-gateway
kubectl describe challenge -n snippet-fullstack-multi-demo-gateway
kubectl logs -n cert-manager deployment/cert-manager --tail=100

kubectl get all,httproute,endpointslices -n snippet-fullstack-multi-demo-app1
kubectl get all,httproute,endpointslices -n snippet-fullstack-multi-demo-app2
```

The first question to ask, every time, is **which of the four combinations
fails** — app1 or app2, page or API. The answer names the layer:

| Symptom | Where to look |
| --- | --- |
| both applications, both halves | the Gateway, DNS, or the cluster add-ons |
| one application, both halves | its listeners, its certificate, its `A` record, its namespace |
| both applications, the API half only | the `URLRewrite` filter / `--root-path` pair, i.e. a 6.4 problem duplicated |
| one application, one half | that Deployment, that Service, that rule |

Failures specific to this example:

- **One challenge succeeds, the other times out with a 404.** The two are
  independent, so this is a per-hostname problem: the second `A` record, most
  often. Reproduce exactly what the ACME server does, on the failing name:
  `curl http://app2.example.com/.well-known/acme-challenge/test`.
- **Both challenges fail, and the solver HTTPRoutes report
  `NoMatchingListenerHostname`.** A `sectionName` was added to the issuer's
  `parentRefs`. Remove it — see *The ACME challenge, twice* above.
- **A route is accepted but nothing reaches the app.** Check its
  `sectionName`: an application route attached to the `http-*` listener
  instead of the `https-*` one is accepted, and then shadowed by the
  redirect.
- **app1 answers with app2's content, or the other way round.** Not possible
  through the Gateway — but very possible in `kubectl`: a command run with
  the wrong `-n` acts on the other application's identically named objects.
  Check the namespace before the manifest.
- **`404` with nginx's HTML on `/api/`.** The `/api` rule did not match and
  the catch-all sent the call to the frontend of that same application. The
  tell is *who* answered: nginx HTML instead of FastAPI's
  `{"detail":"Not Found"}`. See 6.4's troubleshooting, which covers this and
  its mirror image (`{"detail":"Not Found"}` = the filter is missing).
- **`ImagePullBackOff` in one namespace only.** The pull Secret was created
  in the other one, or only once. `kubectl get secret ghcr-secret -n <ns>` in
  both. A `401` in the Pod events also means a placeholder password — see the
  warning about applying `secret.yml` in step 5.
- **The Gateway stays `PROGRAMMED=False` with one Certificate ready.** Normal
  while the other one is missing. `describe` the Gateway and read the
  per-listener conditions rather than the top-level one.

## Let's Encrypt limits with several hostnames

Two hostnames do not come close to any production limit, but the counters are
worth knowing before this pattern grows to ten applications
([official reference](https://letsencrypt.org/docs/rate-limits/), which does
move — Let's Encrypt revised several of these in 2025):

| Limit | Value | Effect here |
| --- | --- | --- |
| Certificates per **registered domain** | 50 / week, sliding | `example.com` counts for *all* its subdomains together. The shared counter to watch as the number of applications grows. |
| **Duplicate certificates** (same exact set of names) | **5 / week** | Counted **per set of names**, so `app1` and `app2` each get their own 5. Repeated `cmctl renew` or Secret deletions burn it fast. |
| Failed validations | 5 / hour / hostname | **Per hostname** too: a misconfigured `app2` does not lock `app1` out. |

Staging limits are far looser, which is the whole reason to start there.

## Adding a third application

Nothing cluster-wide changes, and nothing in the existing two:

```shell
cp -r app2 app3
sed -i 's/app2/app3/g' app3/*.yml app3/*/*.yml
```

then add two listeners to `gateway/gateway.yml`, create the namespace, its
pull Secret and one `A` record. The annotation, the issuers, cert-manager and
both images are untouched — the third certificate appears on its own.

At that point the copy-paste starts to show, and this is the boundary where
templating earns its place: **Helm** or **Kustomize** for the per-application
manifests (the namespace, the hostname and the certificate name are the only
variables), and one of the pull-Secret strategies listed above. The Gateway
itself stays hand-written, because it is the cluster operator's object, not
the applications'.

## Remove the demo

The three namespaces take the applications, the Gateway, both Certificates
and both TLS Secrets with them:

```shell
kubectl delete namespace \
  snippet-fullstack-multi-demo-app1 \
  snippet-fullstack-multi-demo-app2 \
  snippet-fullstack-multi-demo-gateway
```

Deleting the Gateway is what removes the generated Envoy proxy and its
LoadBalancer Service — check that it went away, since on a cloud provider it
costs money:

```shell
kubectl get all -n envoy-gateway-system
```

Remove the two DNS records too.

The ClusterIssuers are cluster-scoped and survive their directory's
namespace. They are only useful to this demo — their solver names its Gateway
— but check that nobody else adopted them first:

```shell
kubectl get certificate --all-namespaces \
  -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,ISSUER:.spec.issuerRef.name'
kubectl delete -f gateway/cluster-issuer.yml
```

The ACME account keys stay behind in cert-manager's namespace; keeping them
is harmless and saves re-registering:

```shell
kubectl delete secret letsencrypt-staging-account-key letsencrypt-account-key -n cert-manager
```

### Shared cluster add-ons: stop and check first

cert-manager, the Envoy Gateway controller and the GatewayClass are
cluster-wide and shared. **Do not delete them if you did not install them, or
if anything else on the cluster still uses them.** The checks, and the
warning about deleting cert-manager's CRDs, are in
[5.2](../5.2_lets_encrypt/README.md#shared-cluster-add-ons-stop-and-check-first):

```shell
kubectl get certificate,issuer --all-namespaces
kubectl get gateway --all-namespaces \
  -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,CLASS:.spec.gatewayClassName'
```

If both lists are empty:

```shell
kubectl delete -f gateway-class/gateway-class.yml
helm uninstall cert-manager --namespace cert-manager
kubectl delete namespace cert-manager
helm uninstall eg --namespace envoy-gateway-system
```

**Keep both images.** `hello-fastapi:1.0` is the app of 6.1 and
`hello-frontend:1.0` the page of 6.4; the examples of chapter 7 start from
exactly this pair.

When you are done with the series, revoke the PAT from *Settings → Developer
settings → Personal access tokens* and clear the local credentials with
`podman logout ghcr.io`.
