# A fullstack app behind one hostname (Gateway API + Let's Encrypt)

[`6.3_stateless_backend_gateway_api_envoy_gateway_with_lets_encrypt`](../6.3_stateless_backend_gateway_api_envoy_gateway_with_lets_encrypt/)
put **one** service on the internet: a FastAPI backend, over HTTPS, under a
real domain name. Here a **second** service joins it — a small nginx serving
a static page — and the page *calls the backend*.

That is the whole example. Two Deployments, two Services, one Gateway, one
certificate, **one hostname**, and a routing rule that sends `/api` to one
Service and everything else to the other:

```
https://my-app.example.com/       -> the page   (nginx)
https://my-app.example.com/api/   -> {"message": "hello"}   (FastAPI)
```

Nothing here is a new Kubernetes *object*: Deployment, Service, Gateway and
HTTPRoute have all been used before. What is new is that an HTTPRoute finally
has a **decision to make**, and the shape of that decision — one hostname,
split by path — is the one that spares you an entire class of problem.
This README explains why, then walks through the deployment as 6.3 did.

It assumes 6.3 has been read: the private registry, the pull Secret,
cert-manager, the ACME HTTP-01 challenge and the gateway-shim are explained
there and are used here unchanged.

## What is in this directory

```
backend/                # the app of 6.1 / 6.2.2 / 6.3, not modified
├── main.py             #   three lines of FastAPI: GET / -> {"message": "hello"}
├── Containerfile       #   -> ghcr.io/<you>/hello-fastapi:1.0  (already built in 6.1)
├── deployment.yml
└── service.yml
frontend/               # the new half
├── index.html          #   one static page, which fetches /api/ and displays it
├── Containerfile       #   -> ghcr.io/<you>/hello-frontend:1.0  (built here)
├── deployment.yml
└── service.yml
gateway-class.yml       # the `eg` GatewayClass (cluster-wide)
cluster-issuer.yml      # Let's Encrypt staging + production ClusterIssuers
gateway.yml             # one Gateway, listeners HTTP:80 and HTTPS:443
http-route.yml          # >>> the interesting file: /api -> backend, / -> frontend
http-redirect-route.yml # 301 http -> https
secret.yml              # the pull Secret as a manifest, for reference only
```

| File | What it is | From |
| --- | --- | --- |
| `backend/main.py`, `backend/Containerfile` | the same app and the same build as 6.1 | 6.3, verbatim |
| `backend/deployment.yml` | the same Deployment, renamed `backend`, plus `--root-path /api` | 6.3, one addition |
| `backend/service.yml` | a ClusterIP Service, `port: 80` → `targetPort: http` | 6.3, renamed |
| `frontend/index.html` | the page: it `fetch`es `/api/` and shows the message | new |
| `frontend/Containerfile` | `nginx:stable-alpine-slim` + that one file | new |
| `frontend/deployment.yml`, `frontend/service.yml` | the backend's, with another image and another port | new |
| `gateway-class.yml` | the `eg` GatewayClass, binding class name → Envoy Gateway controller | identical throughout |
| `cluster-issuer.yml` | the two ClusterIssuers | 6.3, with this demo's namespace |
| `gateway.yml` | the Gateway and its two listeners | 6.3, unchanged |
| `http-route.yml` | **two rules instead of one**, matched on path, one of them rewriting | 6.3's, extended |
| `http-redirect-route.yml` | the 301 http → https | 6.3, verbatim |
| `secret.yml` | the pull Secret as a manifest — for reference, not to be applied | 6.3, verbatim |

The backend image is the one built in 6.1 — same repository, same `1.0` tag,
same `main.py`. If it is still on GHCR, only the frontend has to be built
below.

## What changes, compared to 6.3

| | `6.3` | `6.4` (here) |
| --- | --- | --- |
| Deployments / Services | 1 / 1 | **2 / 2** |
| Images to build | 1 | **2** |
| Pull Secret | 1 | 1 — **shared by both** |
| Hostnames | 1 | 1 — **on purpose** |
| Certificates | 1 | 1 |
| Gateway / listeners | 1 / 2 | 1 / 2 |
| HTTPRoutes | 2 | 2 |
| Rules in the app's route | 1, matching nothing in particular | **2, matched on path** |
| Filters | none | **one `URLRewrite`** |
| Cluster add-ons | Envoy Gateway + cert-manager | the same two |
| Needs a public IP and a real domain | yes | yes |

Adding a whole frontend to a live HTTPS deployment costs: two manifests, one
image, and one rule in an existing route. Nothing about the certificate, the
Gateway, the issuers or the backend image moves. That is worth noticing —
it is the argument for putting the entry point in its own object in the first
place.

## The chain

```
                                   +--> /api/* --[strip /api]--> Service backend  --> Pod (FastAPI, :8000)
                                   |
browser --HTTPS--> Gateway (Envoy) -+
                        ^          |
                        |          +--> /*     ----------------> Service frontend --> Pod (nginx, :80)
              holds the certificate
              for my-app.example.com                 http-route.yml decides, on the path alone
```

Both arrows start at the **browser**. The page is fetched from nginx, then
the JavaScript in it issues a second request, to `/api/`, which travels the
same route back to the Gateway and is dispatched to FastAPI. TLS is
terminated once, by the Gateway; both Pods speak plain HTTP and know nothing
about the certificate.

## One hostname, and what it buys

The single most consequential line of this demo is in `frontend/index.html`:

```js
const response = await fetch("/api/", { cache: "no-store" });
```

A **relative** URL. The browser resolves it against the origin of the page
that contains it — scheme, host and port — giving
`https://my-app.example.com/api/`. Same scheme, same host, same port as the
page itself: this is a **same-origin** request, and the
[same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy)
lets JavaScript read the answer without anyone's permission. No `Origin`
header is sent, no preflight `OPTIONS` is made, and the backend needs no
header, no middleware, no configuration at all. `main.py` is three lines and
one of them is `return`.

Now suppose the backend lived at `https://api.example.com/` instead — a
different host, therefore a different origin. The same `fetch` becomes a
cross-origin request and the browser changes behaviour:

- it adds `Origin: https://my-app.example.com` to the request;
- it **hides the response from the page** unless the answer carries
  `Access-Control-Allow-Origin` naming that origin;
- for anything beyond a simple `GET` — a `PUT`, a `DELETE`, a
  `Content-Type: application/json` body, an `Authorization` header — it first
  sends a preflight `OPTIONS` request and refuses to proceed unless *that*
  is answered with the right `Access-Control-Allow-*` headers;
- cookies are not sent at all unless the request opts in with
  `credentials: "include"` **and** the answer allows it — and then the cookie
  itself needs `SameSite=None; Secure`.

None of it is hard, but all of it is machinery you own forever: a
`CORSMiddleware` in FastAPI, or a CORS filter on the Gateway, with a list of
allowed origins to keep in sync with every environment (production, staging,
review apps, `localhost:5173`). And the failure mode is famously opaque — the
request succeeds, the server logs a `200`, and the browser console says the
response was blocked.

Putting both halves under one hostname deletes that entire category. The cost
is one routing rule. The rest of this README is mostly about that rule.

> A caveat worth stating plainly: CORS is not a security mechanism *for the
> backend*. It restricts what a **browser** lets one page do with another
> origin's answer; `curl`, a mobile app or any server ignores it entirely.
> Same-origin routing removes a browser annoyance, not the need for the
> backend to authenticate its callers.

## Routing by path

`http-route.yml` is 6.3's route with a second rule and an explicit `matches:`
on the first:

```yaml
rules:
  - matches:
      - path:
          type: PathPrefix
          value: /api
    filters:
      - type: URLRewrite
        urlRewrite:
          path:
            type: ReplacePrefixMatch
            replacePrefixMatch: /
    backendRefs:
      - name: backend
        port: 80

  - matches:
      - path:
          type: PathPrefix
          value: /
    backendRefs:
      - name: frontend
        port: 80
```

`PathPrefix` matches whole path **segments**, not characters: `/api` matches
`/api`, `/api/` and `/api/docs`, and does *not* match `/apiary`. (The other
types are `Exact` and the implementation-specific `RegularExpression`.)

### Why this is not ambiguous

`/api/` matches both rules, and the Gateway API does not leave the outcome to
the order of the file. Matches are ranked, and the **first criterion is the
length of the matched path**: `/api` (4 characters) beats `/` (1), always.
Only for rules still tied after that do method, header and query-parameter
matches, and finally order, come into play.

The same ranking applies **across HTTPRoutes**, not merely within one. So
splitting this file into `backend/http-route.yml` and
`frontend/http-route.yml` — one per component, each owned by the team that
owns the Service, possibly in a namespace of its own, as
[`4.3.2`](../4.3.2_gateway_api_envoy_gateway_multi_apps/) lays out — routes
traffic identically. That is the usual production shape. One file is shorter
here, and puts both halves of the decision side by side.

### Stripping `/api`, and the one thing it breaks

The backend's only route is `/`. Forwarded as-is, `GET /api/` would be a
FastAPI `404`. The `URLRewrite` filter removes exactly the prefix that
`matches` matched:

```
/api      ->  /
/api/     ->  /
/api/docs ->  /docs
```

so the application receives what it expects and remains reusable behind any
prefix — which is why its image is still 6.3's, byte for byte.

The catch is that the app is now **wrong about its own URLs**. It is reached
at `https://my-app.example.com/api/docs` but sees `/docs`, and any absolute
path it generates comes out missing the prefix. FastAPI generates several:
the Swagger UI at `/docs` builds the URL of the schema it loads, and without
help it builds `/openapi.json` — a path that does not start with `/api`,
which the Gateway therefore hands to the **frontend**, which serves its index
page, and the documentation stays empty forever.

The fix is one line in `backend/deployment.yml`, not in the image:

```yaml
command: [fastapi, run, main.py, --host, 0.0.0.0, --port, "8000", --root-path, /api]
```

`--root-path` is how an ASGI application is told *"you are published under
this prefix"*. Routing is unaffected — the app still serves `/` — but every
URL it builds is prefixed, so `/api/docs` finds `/api/openapi.json` and
works. It belongs in the manifest rather than in the `Containerfile`
precisely because the prefix is a deployment decision: the same image is
served at `/api` here and could be served at `/` tomorrow.

This is the general rule, well beyond FastAPI: **a prefix-stripping proxy and
an application that generates links must agree.** The equivalent knobs are
`root_path` (ASGI), `APPLICATION_ROOT` (Flask/WSGI), `FORCE_SCRIPT_NAME`
(Django), `basePath` (Next.js). Skipping it is the reason so many
reverse-proxied admin panels come out with broken CSS.

Two related settings from 6.3 are worth re-reading in that light: the app
also cannot know the *scheme* it was reached with unless uvicorn is told to
trust Envoy's `X-Forwarded-Proto` (`FORWARDED_ALLOW_IPS`, see 6.3). Nothing
here needs it, because nothing here builds an absolute URL.

### The alternative: let the application own the prefix

The filter can be dropped entirely, and there are two ways to do it:

```python
app = FastAPI(root_path="/api")          # declare the prefix, keep serving "/"
```

```python
router = APIRouter(prefix="/api")        # really serve /api/... , no root_path
```

Both work, and neither is wrong. Three designs, then:

| | who strips `/api` | the image knows its public path | route |
| --- | --- | --- | --- |
| **used here** — `URLRewrite` + `--root-path /api` | the Gateway | no | filter |
| `FastAPI(root_path="/api")`, no filter | Starlette, on the way in | yes | plain |
| `APIRouter(prefix="/api")`, no filter | nobody, the app serves it | yes | plain |

This example takes the first because its image is **shared with four other
directories** (6.1, 6.2.1, 6.2.2, 6.3), where the same app is served at `/`
with no prefix at all. An image that declares `root_path="/api"` would still
answer there — but it would advertise a `/api` prefix that does not exist in
those demos, and their OpenAPI schema would gain a `servers: [{"url":
"/api"}]` entry that is simply false. Keeping the image neutral about where
it is mounted is what lets five examples share one tag.

The general principle behind that: **the mount point is a deployment
decision, not an application one.** Stripping at the edge keeps it in the
manifest, next to the hostname and the certificate, which are deployment
decisions too. If you prefer the application to own it, the way to keep the
same property is to read it from the environment —
`FastAPI(root_path=os.environ.get("ROOT_PATH", ""))` — and set it in
`deployment.yml`, which is `--root-path` by another name.

### `--root-path` and `root_path=` are not interchangeable

Worth knowing before swapping one for the other, because the failure is a
flat `404` with nothing in any log to explain it. The two settings look like
synonyms — the FastAPI documentation itself calls passing `root_path` to the
app "the equivalent" of the command-line option — and for URL *generation*
they are. For **routing** they are not, because they are read by two
different programs:

- `--root-path /api` is uvicorn's. Uvicorn **prepends** it to the path before
  handing the request to the app (`full_path = self.root_path + path`), which
  is what the ASGI specification asks for: `scope["path"]` is meant to
  include `root_path`. So this flag *assumes the proxy already stripped the
  prefix* and merely puts it back for the app's benefit.
- `root_path="/api"` on the `FastAPI` object is Starlette's. It sets
  `scope["root_path"]` and leaves the path alone, and Starlette then removes
  the prefix when matching routes (`get_route_path`).

Hence the asymmetry, measured on the versions pinned in `backend/Containerfile`
(FastAPI 0.141.1, Starlette 1.6.0, uvicorn 0.53.0):

| what reaches the app server | `--root-path /api` | `FastAPI(root_path="/api")` |
| --- | --- | --- |
| `GET /` (the Gateway stripped) | `200` | `200` |
| `GET /api/` (it did not) | **`404`** — uvicorn makes it `/api/api/` | `200` |

So the configuration used here — filter **and** `--root-path` — is a matched
pair: remove the filter without also moving the setting into the code and the
backend returns `404` on every call. The second column is the more forgiving
of the two, which is a fair argument in its favour for an application you
control end to end.

Note also that this area has moved: Starlette's handling of `root_path` in
routing was reworked several times (encode/starlette #2352, #2400, #2600).
Behaviour that depends on it deserves the version pin that
`backend/Containerfile` already has, and a quick `curl` after an upgrade.

## Who talks to whom

Worth being precise, because "frontend and backend" suggests a conversation
that does not happen here:

```
browser  --GET /------>  Gateway --> Service frontend --> nginx Pod
browser  --GET /api/-->  Gateway --> Service backend  --> FastAPI Pod
```

The nginx Pod never calls the FastAPI Pod. Both requests come from the
browser, over the internet, into the same Gateway. nginx serves a file and
has never heard of the backend — grep its `Containerfile` for it.

Two consequences:

- **The backend is public.** It is on the internet with an HTTPS URL, and
  `curl https://my-app.example.com/api/` works from anywhere. Being "the
  backend" is not a property Kubernetes knows about; if it must not be
  reachable from outside, the thing to change is the route, not the label.
- **The two halves scale independently**, and a frontend replica adds no load
  to the backend.

The other design puts nginx in the middle — a reverse proxy, or a
*backend-for-frontend*:

```nginx
location /api/ { proxy_pass http://backend/; }   # `backend` = the Service's DNS name
```

Then only the frontend is routed at the Gateway, the backend Service is never
exposed, and the browser still sees a single origin, so CORS is still absent.
The price: an extra hop for every API byte, and the backend's address baked
into the frontend image — moving the API means rebuilding it. That is the
shape used from [`7.1_sqlite_volume`](../7.1_sqlite_volume/) on, where it
also demonstrates in-cluster service-to-service DNS
(`backend.snippet-fullstack-demo.svc.cluster.local`, or just `backend` from
within the namespace).

Neither is more correct. Routing at the Gateway keeps the images ignorant of
each other and the topology in one file; proxying in the frontend keeps the
API off the public internet. This example takes the first, because the
Gateway API is the subject.

## Prerequisites

Exactly 6.3's — a container engine, a GitHub account, a cluster whose Gateway
gets a **public IP** reachable on ports 80 and 443, and a **domain name you
own** whose `A` record will point at it. Let's Encrypt validates the domain
from the internet, so minikube and kind cannot be used here, and
`curl --resolve` or `/etc/hosts` tricks do not help: the ACME server resolves
the name itself.

Envoy Gateway (step 4) and cert-manager (step 5) are installed below, with
the checks to make *before* installing anything cluster-wide.

Replace `jeremiedecock` with your own GitHub username, `my-app.example.com`
with your own domain and `you@example.com` with your address:

```shell
sed -i 's/jeremiedecock/your-github-username/g' backend/deployment.yml frontend/deployment.yml
sed -i 's/my-app\.example\.com/www.your-domain.com/g' gateway.yml http-route.yml http-redirect-route.yml
sed -i 's/you@example\.com/your-address@your-domain.com/g' cluster-issuer.yml
```

## 1. Create a Personal Access Token

If 6.1 or 6.3 is still fresh, `$GHCR_TOKEN` is set and you are logged in —
skip to step 2.

Otherwise create a **PAT (classic)**, as described in
[Authenticating with a personal access token](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-with-a-personal-access-token-classic),
with the scopes `read:packages`, `write:packages`, `delete:packages` and
`repo`. The cluster only ever needs `read:packages`. Keep it in your
`.bashrc`:

```shell
export GHCR_TOKEN=ghp_...
```

Then log in, with the token on stdin so it stays out of your shell history:

```shell
echo $GHCR_TOKEN | podman login ghcr.io -u jeremiedecock --password-stdin
```

## 2. Build and push the two images

The backend is the image of 6.1, unchanged — if it is still on GHCR, skip
straight to the frontend:

```shell
podman build -t ghcr.io/jeremiedecock/hello-fastapi:1.0 backend/
podman push ghcr.io/jeremiedecock/hello-fastapi:1.0
```

The frontend is new. It is a stock nginx with one file copied into it, so the
build is a few seconds and the layer is a few kilobytes:

```shell
podman build -t ghcr.io/jeremiedecock/hello-frontend:1.0 frontend/
podman push ghcr.io/jeremiedecock/hello-frontend:1.0
```

(With `docker`, add `-f backend/Containerfile` / `-f frontend/Containerfile`:
Docker looks for a file named `Dockerfile` by default.)

Both packages are **private** by default at <https://github.com/jeremiedecock?tab=packages>,
hence the pull Secret in the next step. Note that it is one Secret for two
images: the credentials belong to the *registry*, not to a repository.

Try the frontend locally before shipping it — it will show its error state,
since nothing serves `/api/` on your laptop, which is itself a useful thing
to have seen once:

```shell
podman run --rm -p 8080:80 ghcr.io/jeremiedecock/hello-frontend:1.0
```

## 3. Create the namespace and the pull Secret

```shell
kubectl create namespace snippet-fullstack-demo
```

Add `-n snippet-fullstack-demo` to every `kubectl` command below.

```shell
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username='jeremiedecock' \
  --docker-password="$GHCR_TOKEN" \
  -n snippet-fullstack-demo
```

That `-n` is not optional: a pull Secret is a **namespaced** object, and the
kubelet only looks for it in the namespace of the Pod that references it.
Both Deployments name this one in `imagePullSecrets`.

```shell
kubectl get secret ghcr-secret -n snippet-fullstack-demo
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
`gateway.yml` and skip the apply. Otherwise:

```shell
kubectl apply -f gateway-class.yml
kubectl get gatewayclass
```

`ACCEPTED` must read `True` — `False` or `Unknown` means the controller is
not running.

## 5. Install cert-manager

Another cluster-wide add-on, so again, look first:

```shell
kubectl get deployments -n cert-manager
kubectl api-resources --api-group=cert-manager.io
```

If it is already installed, skip to *Check the Gateway API integration* — the
integration still has to be enabled, and it is off by default. Otherwise:

```shell
helm install cert-manager oci://quay.io/jetstack/charts/cert-manager \
  --version v1.21.2 \
  --namespace cert-manager --create-namespace \
  --set crds.enabled=true \
  --set config.gatewayAPI.enabled=true
```

`config.gatewayAPI.enabled=true` is what makes cert-manager look at Gateway
objects at all. **Without it, the annotation in `gateway.yml` is ignored and
nothing happens** — no Certificate, no error, no event.

```shell
kubectl wait --timeout=5m -n cert-manager deployment --all --for=condition=Available
```

### Check the Gateway API integration

cert-manager checks for the Gateway API CRDs **only at startup**, so restart
it if it was installed before Envoy Gateway:

```shell
kubectl rollout restart deployment cert-manager -n cert-manager
```

This should print `true`:

```shell
kubectl get configmap cert-manager -n cert-manager -o yaml | grep -A2 gatewayAPI
```

See 5.2 for the details.

## 6. Create the issuers

```shell
kubectl apply -f cluster-issuer.yml
```

Two ClusterIssuers, `letsencrypt-staging` and `letsencrypt`, differing only by
the ACME server URL, both naming **this demo's Gateway and namespace** in
their HTTP-01 solver. **Always start with staging**, which `gateway.yml`
does: its certificates are untrusted, but its
[rate limits](https://letsencrypt.org/docs/rate-limits/) are loose, whereas
production's are easy to burn through while a DNS record is still wrong.

```shell
kubectl get clusterissuer
```

## 7. Deploy the demo

```shell
kubectl apply \
  -f backend/deployment.yml \
  -f backend/service.yml \
  -f frontend/deployment.yml \
  -f frontend/service.yml \
  -f gateway.yml \
  -f http-route.yml \
  -f http-redirect-route.yml \
  -n snippet-fullstack-demo
```

(`kubectl apply -f backend/ -f frontend/` also works — a directory is read
for `.yml`, `.yaml` and `.json` files only, so `main.py` and the
`Containerfile`s are ignored.)

Wait for both images to be pulled and both readiness probes to pass:

```shell
kubectl rollout status deployment/backend  -n snippet-fullstack-demo
kubectl rollout status deployment/frontend -n snippet-fullstack-demo
```

Then wait for the Gateway's `ADDRESS` column to be populated (`Ctrl+C` to
stop watching):

```shell
kubectl get gateway -n snippet-fullstack-demo --watch
```

`PROGRAMMED` will read `False` at this stage, and that is expected: the HTTPS
listener points at a Secret that does not exist yet. The `http` listener is
already serving, which is what matters — it is the one that will carry the
ACME challenge.

Check that both hops of both rules resolved. Each Service must have an
endpoint, and the route must have been accepted with its backends resolved:

```shell
kubectl get endpointslices -n snippet-fullstack-demo
kubectl describe httproute my-route -n snippet-fullstack-demo
```

Look for `Accepted: True` and `ResolvedRefs: True` under `Parents`. With two
`backendRefs` now, `ResolvedRefs` covers both: a typo in either Service name
turns it `False`, and the *other* rule keeps working — which is exactly the
half-broken state to expect if only one of the two halves misbehaves.

### Point DNS at the Gateway

```shell
GATEWAY_IP=$(kubectl get gateway my-gateway -n snippet-fullstack-demo \
  -o jsonpath='{.status.addresses[0].value}')
echo $GATEWAY_IP
```

Create an `A` record for your domain pointing at it (or a `CNAME` if your
provider hands out a hostname), then wait for it to propagate. Do not skip
this check — a stale record is the single most common cause of a failing
challenge:

```shell
dig +short my-app.example.com
curl -i http://my-app.example.com/
```

The `curl` should answer `301` towards `https://`, proving the `http`
listener is reachable from the outside on port 80.

## 8. Watch the certificate being issued

Unchanged from 6.3 — the certificate belongs to the Gateway and knows nothing
about how many Services sit behind it:

```shell
kubectl get certificate -n snippet-fullstack-demo --watch
```

Nobody wrote that object: cert-manager's gateway-shim generated it from the
annotated listener, and named it after the Secret.

```shell
kubectl get certificate,certificaterequest,order,challenge -n snippet-fullstack-demo
kubectl describe challenge -n snippet-fullstack-demo
```

`kubectl describe challenge` is the single most useful command when this
hangs: its status message is the verbatim answer Let's Encrypt got when it
fetched the token.

Once `READY` is `True`, the namespace holds **two Secrets of two different
kinds**: `ghcr-secret`, which you created to *pull* the images, and `my-tls`,
which cert-manager created to *serve* them:

```shell
kubectl get secret -n snippet-fullstack-demo
kubectl get secret my-tls -n snippet-fullstack-demo \
  -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -subject -issuer -dates
```

The issuer reads `(STAGING)` something, from Let's Encrypt's test hierarchy.
The Gateway should now be fully programmed:

```shell
kubectl get gateway -n snippet-fullstack-demo
```

## 9. Test both halves, with the staging certificate

`curl` refuses the staging certificate, as every client does — `-k` skips the
check and confirms that everything but the trust chain works:

```shell
curl -k https://my-app.example.com/api/
```

```json
{"message":"hello"}
```

```shell
curl -ks https://my-app.example.com/ | head -5
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
```

Two Services, one hostname, one certificate. The path did all the work.

The rewrite is easiest to see on a path that exists on neither side —
compare who answers, and in which language:

```shell
curl -k https://my-app.example.com/api/nope   # FastAPI:  {"detail":"Not Found"}
curl -k https://my-app.example.com/nope       # nginx:    <html>404 Not Found</html>
```

And the documentation, which is the reason `--root-path` is in
`backend/deployment.yml` — note the `servers` entry in the schema, which is
the app telling clients where it really lives:

```shell
curl -k https://my-app.example.com/api/openapi.json | head -c 200
```

Finally the redirect on port 80, which now that the challenge is over catches
everything:

```shell
curl -I http://my-app.example.com/
```

## 10. Switch to the production issuer

Only once the above works end to end:

```shell
sed -i 's|cert-manager.io/cluster-issuer: letsencrypt-staging|cert-manager.io/cluster-issuer: letsencrypt|' gateway.yml
kubectl apply -f gateway.yml -n snippet-fullstack-demo
```

cert-manager notices the `issuerRef` of the Certificate no longer matches and
re-issues it through the same challenge:

```shell
kubectl get certificate -n snippet-fullstack-demo --watch
kubectl get secret my-tls -n snippet-fullstack-demo \
  -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -subject -issuer -dates
```

And plain `curl`, with no flag at all, finally works:

```shell
curl https://my-app.example.com/api/
```

## 11. Open it in a browser

This is the step the whole series was heading towards, and the only one that
cannot be done with `curl`, because the point is what the *browser* does:

**<https://my-app.example.com/>**

A padlock, no warning, and a page that says `hello` — a word that is not in
the HTML. Open the developer tools, *Network* tab, and reload:

- two requests, `/` and `/api/`, both to `my-app.example.com`, both `200`;
- **no `OPTIONS` preflight** before the second one, and no `Origin` header on
  it — the browser did not consider it a cross-origin request, so it asked no
  permission;
- no `Access-Control-Allow-Origin` in the answer, because none was needed.

That absence is the deliverable. Change the `fetch` in `index.html` to an
absolute URL on another host and every one of those three lines turns into
work.

`https://my-app.example.com/api/docs` gives the Swagger UI of the backend,
under the same padlock — and the schema loads, which it would not have done
without `--root-path`.

## Scaling and updating

Each half scales on its own, and neither the Gateway, the route nor the
certificate is touched by any of it:

```shell
kubectl scale deployment/backend --replicas=3 -n snippet-fullstack-demo
for i in $(seq 6); do curl -s https://my-app.example.com/api/ > /dev/null; done
kubectl logs -l app=backend --prefix --tail=3 -n snippet-fullstack-demo
```

The log lines are spread across the three Pods: the `backend` Service
load-balanced them. Note the path in those lines — `"GET / HTTP/1.1"`, not
`/api/`: what the application sees is what the filter left of the request.

Updating one half leaves the other running:

```shell
podman build -t ghcr.io/jeremiedecock/hello-frontend:1.0.1 frontend/
podman push ghcr.io/jeremiedecock/hello-frontend:1.0.1
kubectl set image deployment/frontend \
  frontend=ghcr.io/jeremiedecock/hello-frontend:1.0.1 \
  -n snippet-fullstack-demo
kubectl rollout status deployment/frontend -n snippet-fullstack-demo
```

`frontend=` is the **container** name from `frontend/deployment.yml`, and the
new tag matters: overwriting `1.0` would change what every other demo pulls.
`kubectl rollout undo deployment/frontend` reverts. Scale back down before
moving on:

```shell
kubectl scale deployment/backend --replicas=1 -n snippet-fullstack-demo
```

## When it does not work

6.3's two chains still apply — **a TLS error or no certificate** is the
cert-manager chain, **a `404`, a `503` or an `ImagePullBackOff`** the routing
chain — and this example adds a third symptom of its own: *the page loads but
the message does not*.

### The page loads, the message does not

The browser is the debugger here: open the developer tools and read the
`/api/` request in the *Network* tab. The page itself came from nginx, so the
frontend half is proven working; what is left is the API half of the route.

- **`404`, with nginx's HTML in the body.** The `/api` rule did not match and
  the catch-all sent the call to the frontend. The tell is *who* answered:
  nginx HTML instead of FastAPI's `{"detail":"Not Found"}`. Check the
  spelling of `value: /api` in the route, and remember `PathPrefix` matches
  whole segments — a call to `/apiv2/` never matches `/api`.
- **`404`, with `{"detail":"Not Found"}` in the body.** The opposite: the
  rule matched, FastAPI answered, and the path it received is not one it
  serves. The `URLRewrite` filter is missing, misspelled, or unsupported by
  the controller — without it FastAPI receives `/api/` and knows only `/`.
  Confirm with `kubectl logs -l app=backend`, which prints the path as the
  app saw it.
- **`503`.** The rule matched and the backend has no ready endpoint:
  `kubectl get endpointslices -n snippet-fullstack-demo`.
- **The message is `hello` but the page still looks broken.** A browser
  cache. `Ctrl+Shift+R`, or check that `imagePullPolicy: Always` actually
  pulled the new frontend image.
- **A CORS error in the console.** Then the request did not go where this
  demo sends it: some absolute URL is left in `index.html`, or the page was
  opened from a `file://` path or from `localhost` while the API is remote.
  Nothing in this setup can produce a CORS error by itself — that is its
  whole purpose.

### The routing chain

```shell
kubectl describe httproute my-route -n snippet-fullstack-demo
kubectl get endpointslices -n snippet-fullstack-demo
kubectl describe pod -l app=frontend -n snippet-fullstack-demo | tail -20
```

- **`404` from Envoy for everything.** The request reached the proxy and
  matched no route at all: the hostname queried is not the one in
  `hostnames:`, or `sectionName` names a listener that does not exist —
  `Accepted: False` with `NoMatchingParent`.
- **`503`.** `ResolvedRefs: False` / `BackendNotFound` means a wrong Service
  name or port in `backendRefs` (`80` here, never `8000`); a resolved ref
  with an empty `endpointslices` listing means no Pod is ready.
- **Pods in `ImagePullBackOff`.** The registry side, as in 6.1. A `401` in
  the Pod events means the Secret is missing, misnamed, **in another
  namespace**, or built with a `--docker-server` other than exactly
  `ghcr.io`. Note which of the two Pods is failing: the frontend image is the
  new one, and the most likely to have been forgotten at the `podman push`.
- **Pods `Running` but `0/1 READY`.** The readiness probe is failing;
  `kubectl describe pod` gives the status code it got.

### The certificate chain

Unchanged from 6.3 and 5.2. Each object's `status` names the next one to look
at:

```shell
kubectl describe gateway my-gateway -n snippet-fullstack-demo
kubectl describe certificate my-tls -n snippet-fullstack-demo
kubectl describe certificaterequest -n snippet-fullstack-demo
kubectl describe order -n snippet-fullstack-demo
kubectl describe challenge -n snippet-fullstack-demo
kubectl logs -n cert-manager deployment/cert-manager --tail=100
```

The one trap worth repeating, because the frontend's catch-all rule makes it
look new: the ACME challenge is served over the **`http` listener**, by a
temporary HTTPRoute that cert-manager creates with an `Exact` path match on
`/.well-known/acme-challenge/<token>`. An `Exact` match outranks any prefix,
so neither the redirect route nor `/`'s catch-all can hide it. If a challenge
returns the frontend's index page, the solver route is not there at all —
look at the cert-manager logs, not at `http-route.yml`.

## Remove the demo

```shell
kubectl delete \
  -f http-redirect-route.yml \
  -f http-route.yml \
  -f gateway.yml \
  -f frontend/service.yml \
  -f frontend/deployment.yml \
  -f backend/service.yml \
  -f backend/deployment.yml \
  -n snippet-fullstack-demo

kubectl delete namespace snippet-fullstack-demo
```

Deleting the namespace takes the `ghcr-secret` pull Secret, the Certificate
and the `my-tls` Secret with it. Remove the DNS record you created too.
Deleting the Gateway is what removes the generated Envoy proxy and its
LoadBalancer Service — check that it went away, since on a cloud provider it
costs money:

```shell
kubectl get all -n envoy-gateway-system
```

The ClusterIssuers are cluster-scoped, so they survive the namespace and have
to be deleted explicitly. They are only useful to this demo — their solver
names its Gateway — but check that nobody else adopted them first:

```shell
kubectl get certificate --all-namespaces \
  -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,ISSUER:.spec.issuerRef.name'
kubectl delete -f cluster-issuer.yml
```

The ACME account keys stay behind, in cert-manager's namespace. Keeping them
is harmless and saves re-registering:

```shell
kubectl delete secret letsencrypt-staging-account-key letsencrypt-account-key -n cert-manager
```

### Shared cluster add-ons: stop and check first

cert-manager, the Envoy Gateway controller and the GatewayClass are
cluster-wide and shared. **Do not delete them if you did not install them, or
if anything else on the cluster still uses them:**

```shell
kubectl get certificate,issuer --all-namespaces
kubectl get gateway --all-namespaces \
  -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,CLASS:.spec.gatewayClassName'
```

If both lists are empty:

```shell
helm uninstall cert-manager --namespace cert-manager
kubectl delete namespace cert-manager
kubectl delete -f gateway-class.yml
helm uninstall eg --namespace envoy-gateway-system
```

`helm uninstall` leaves the cert-manager CRDs in place on purpose, because
deleting a CRD garbage-collects every object of that kind — every
Certificate, Issuer and ClusterIssuer on the cluster.

**Keep both images.** `hello-fastapi:1.0` is the app of 6.1, and
`hello-frontend:1.0` is the page built here; the next examples start from
exactly this pair.

When you are done with the series, revoke the PAT from *Settings → Developer
settings → Personal access tokens* and clear the local credentials with
`podman logout ghcr.io`.
