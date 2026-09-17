# Your own image, served over HTTPS with Let's Encrypt (Gateway API + cert-manager)

This example is the meeting point of two earlier ones, and assumes both have
been read:

- [`6.2.2_stateless_backend_gateway_api_envoy_gateway`](../6.2.2_stateless_backend_gateway_api_envoy_gateway/)
  — **your own FastAPI image**, pulled from a private registry (GHCR) and
  exposed with a **Gateway** and an **HTTPRoute**, over plain HTTP;
- [`5.2_lets_encrypt`](../5.2_lets_encrypt/) — a stock nginx served over
  **HTTPS**, with a **Let's Encrypt** certificate that
  [cert-manager](https://cert-manager.io/) obtains, installs and renews on its
  own.

Here, **your own image is served over HTTPS under a real domain name, with a
publicly trusted certificate** — the first example of the series that looks
like something you would actually put online.

Nothing conceptual is new: the private registry and the pull Secret are
explained in [`6.1`](../6.1_private_docker_registry_ghcr/) and 6.2.2, the
Gateway API in [`4.3.1`](../4.3.1_gateway_api_envoy_gateway/), and
cert-manager, the
ACME HTTP-01 challenge and the gateway-shim in 5.2. This README does not
repeat them; it gives the full walkthrough, but explains only what changes
when the two examples are combined.

## What is in this directory

| File | What it is | From |
| --- | --- | --- |
| `main.py`, `Containerfile` | the same app and the same build as 6.1, unchanged | 6.2.2, verbatim |
| `deployment.yml` | a Deployment of the GHCR image, with `imagePullSecrets`, a named port `http` and a readiness probe | 6.2.2, verbatim |
| `service.yml` | a ClusterIP Service, `port: 80` → `targetPort: http` | 6.2.2, verbatim |
| `secret.yml` | the pull Secret as a manifest — for reference, not to be applied (see 6.1) | 6.2.2, verbatim |
| `gateway-class.yml` | the `eg` GatewayClass, binding class name → Envoy Gateway controller (cluster-wide) | identical in both |
| `cluster-issuer.yml` | two ClusterIssuers, Let's Encrypt staging and production | 5.2, with this demo's namespace |
| `gateway.yml` | a Gateway with an `HTTP:80` **and** an `HTTPS:443` listener, plus the `cert-manager.io/cluster-issuer` annotation | 5.2 |
| `http-route.yml` | the app's route, attached to the `https` listener | 5.2's, pointing at 6.2.2's Service |
| `http-redirect-route.yml` | a 301 `http` → `https`, attached to the `http` listener | 5.2, verbatim |

The application half is byte-for-byte that of 6.2.2, and the image is the one
built in 6.1 — same repository, same `1.0` tag, same `main.py`. If it is still
on GHCR, steps 1 and 2 below are a no-op and you can jump to *3. Create the
namespace and the pull Secret*.

## What changes

| | `6.2.2` | `5.2` | `6.3` (here) |
| --- | --- | --- | --- |
| The app | your FastAPI image, from GHCR | stock nginx, public | **your FastAPI image, from GHCR** |
| Pull Secret | yes | no | **yes** |
| Listeners on the Gateway | one, `HTTP:80` | two, `HTTP:80` + `HTTPS:443` | **two** |
| Listener `hostname` | none (any host) | required | **required** |
| Certificate | none | Let's Encrypt | **Let's Encrypt** |
| HTTPRoutes | 1 | 2 (app + redirect) | **2** |
| Cluster add-ons | Envoy Gateway | Envoy Gateway + cert-manager | **both** |
| Needs a public IP | no | **yes** | **yes** |
| Needs a real domain name | no | **yes** | **yes** |
| Testable on minikube/kind | yes | no | **no** |

The last three rows are the real cost of this example. Let's Encrypt validates
the domain by connecting to it **from the internet**, so a laptop cluster
cannot work here, and the `curl --resolve` or `/etc/hosts` tricks that were
fine in [`5.1_tls`](../5.1_tls/) are useless: Let's Encrypt resolves the name
itself, from its own servers.

Concretely, compared to 6.2.2, four things are new — exactly the four that 5.2
added to 4.3.1:

1. **cert-manager** is installed on the cluster, with its Gateway API
   integration enabled;
2. a **ClusterIssuer** (`cluster-issuer.yml`) describes the Let's Encrypt
   account and how domain ownership is proven;
3. `gateway.yml` gains an **HTTPS listener** and one **annotation**,
   `cert-manager.io/cluster-issuer`, which is the entire trigger;
4. the routes gain hostnames, split across the two listeners, and a redirect
   route sends plain HTTP to HTTPS.

Nothing in `deployment.yml` or `service.yml` moves. That is the point.

## The chain

```
internet --HTTPS--> Gateway (Envoy, holds the certificate) --HTTP--> Service --> Pod
                         ^                                              ^        (FastAPI,
                gateway.yml: listeners :80 and :443          service.yml: port 80  :8000)
                http-route.yml: https -> Service               -> targetPort http
                http-redirect-route.yml: http -> 301
                         ^
                cert-manager fills the `my-tls` Secret,
                triggered by the annotation on the Gateway
```

TLS is terminated by the **Gateway**, not by the application: the Envoy proxy
decrypts incoming traffic and forwards plain HTTP to the Service, on port 80,
exactly as in 6.2.2. Certificates live in one place, owned by whoever operates
the Gateway.

### The port chain, again

Unchanged from 6.2.2, and still the most common source of silent failures.
`backendRefs[].port` in the HTTPRoute is the **Service** port, not the
container port — and adding HTTPS in front changes none of these numbers:

| Where | Field | Value |
| --- | --- | --- |
| `deployment.yml` | `containerPort` | `8000`, named `http` |
| `service.yml` | `targetPort` | `http` (the name, resolved per Pod) |
| `service.yml` | `port` | `80` — what the Service answers on |
| `http-route.yml` | `backendRefs[].port` | `80` — must equal the Service's `port` |

The `443` of the HTTPS listener belongs to the Gateway alone and appears
nowhere else.

### The app never sees the certificate

The FastAPI process speaks plain HTTP on `0.0.0.0:8000` and is unaware that
anything is encrypted. Two consequences worth knowing, neither of which
affects this demo:

- **The readiness probe is unaffected.** The kubelet queries `/` on the Pod's
  own IP, inside the cluster, in plain HTTP — it never goes through the
  Gateway, so no certificate and no hostname are involved.
- **Absolute URLs are the app's business.** Envoy forwards
  `X-Forwarded-Proto: https`, but a backend only trusts that header if it is
  told to. `fastapi run` enables uvicorn's proxy-header handling, whose
  `--forwarded-allow-ips` defaults to `127.0.0.1` — and Envoy is a different
  Pod with a different IP, so by default the header is ignored and anything
  the app builds by hand comes out as `http://`. The moment that matters
  (redirects, OAuth callbacks, absolute links), set the trusted source on the
  container:

  ```yaml
  env:
    - name: FORWARDED_ALLOW_IPS
      value: "*"
  ```

  `*` is only reasonable because nothing but the Gateway can reach the Pod;
  on an open network it would let any client claim any scheme and any client
  IP. `main.py` returns a constant JSON object and builds no URL, so nothing
  here needs it.

## Prerequisites

- **A container engine** — [Podman](https://podman.io/) below; `docker` works
  identically, with `-f Containerfile` added to the build.
- **A GitHub account**, for GHCR.
- **A cluster whose Gateway gets a public IP**, reachable from the internet on
  ports **80 and 443**. In practice: a cloud cluster. Check that your
  provider's firewall or security groups let port 80 through — it is often the
  forgotten one, and HTTP-01 needs exactly that.
- **A domain name you own**, with a DNS `A` record pointing at the Gateway
  address. Chicken and egg: the address only exists once the Gateway is
  applied, so the order is *apply the Gateway → read its address → create the
  DNS record → let cert-manager work*. The walkthrough below follows that
  order.
- **Envoy Gateway and the `eg` GatewayClass** (step 4), and **cert-manager**
  (step 5), both installed below — with the checks to make *before* installing
  anything cluster-wide.

Replace `jeremiedecock` with your own GitHub username, `my-app.example.com`
with your own domain and `you@example.com` with your address:

```shell
sed -i 's/jeremiedecock/your-github-username/g' deployment.yml
sed -i 's/my-app\.example\.com/www.your-domain.com/g' gateway.yml http-route.yml http-redirect-route.yml
sed -i 's/you@example\.com/your-address@your-domain.com/g' cluster-issuer.yml
```

## 1. Create a Personal Access Token

If 6.1 or 6.2.2 is still fresh, `$GHCR_TOKEN` is set and you are logged in —
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

Same image and same tag as 6.1 and 6.2.2:

```shell
podman build -t ghcr.io/jeremiedecock/hello-fastapi:1.0 .
podman push ghcr.io/jeremiedecock/hello-fastapi:1.0
```

Check the pushed image at <https://github.com/jeremiedecock?tab=packages> —
it is **private**, hence the next step.

## 3. Create the namespace and the pull Secret

```shell
kubectl create namespace snippet-backend-letsencrypt-demo
```

Add `-n snippet-backend-letsencrypt-demo` to every `kubectl` command below.

The Secret is detailed in
[6.1](../6.1_private_docker_registry_ghcr/#4-create-the-pull-secret); in
short, it wraps the token in the `dockerconfigjson` format the kubelet
expects, and `deployment.yml` names it in `imagePullSecrets`:

```shell
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username='jeremiedecock' \
  --docker-password="$GHCR_TOKEN" \
  -n snippet-backend-letsencrypt-demo
```

That `-n` is not optional: a pull Secret is a **namespaced** object, and the
kubelet only looks for it in the namespace of the Pod that references it.

```shell
kubectl get secret ghcr-secret -n snippet-backend-letsencrypt-demo
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
kubectl get gatewayclass
```

`ACCEPTED` must read `True` — `False` or `Unknown` means the controller is not
running.

## 5. Install cert-manager

cert-manager is a cluster-wide add-on shared by every application on the
cluster, so check before installing anything:

```shell
kubectl get deployments -n cert-manager
kubectl api-resources --api-group=cert-manager.io
```

If it is already there, skip the `helm install` and jump to *Check the Gateway
API integration* — the integration still has to be enabled, and it is off by
default. Otherwise, install the chart, its CRDs and the Gateway API
integration in one go:

```shell
helm install cert-manager oci://quay.io/jetstack/charts/cert-manager \
  --version v1.21.2 \
  --namespace cert-manager --create-namespace \
  --set crds.enabled=true \
  --set config.gatewayAPI.enabled=true
```

- `crds.enabled=true` installs the `Certificate`, `Issuer`, `ClusterIssuer`,
  `Order`, `Challenge`... CRDs along with the controller.
- `config.gatewayAPI.enabled=true` is what makes cert-manager look at Gateway
  objects at all. **Without it, the annotation in `gateway.yml` is ignored and
  nothing happens** — no Certificate, no error, no event. (This nested
  spelling was introduced in cert-manager 1.21; older releases use
  `config.enableGatewayAPI=true`, still accepted but deprecated.)

```shell
kubectl wait --timeout=5m -n cert-manager deployment --all --for=condition=Available
```

### Check the Gateway API integration

cert-manager checks for the Gateway API CRDs **only at startup**. If it was
installed before Envoy Gateway, it will never notice them, so restart it after
any such change:

```shell
kubectl rollout restart deployment cert-manager -n cert-manager
```

Confirm the setting actually took effect — this should print `true`:

```shell
kubectl get configmap cert-manager -n cert-manager -o yaml | grep -A2 gatewayAPI
```

See 5.2 for the details, and the
[cert-manager installation documentation](https://cert-manager.io/docs/installation/helm/)
for the other installation methods.

## 6. Create the issuers

```shell
kubectl apply -f cluster-issuer.yml
```

`cluster-issuer.yml` declares two ClusterIssuers, `letsencrypt-staging` and
`letsencrypt`, differing only by the ACME server URL, and both naming **this
demo's Gateway** in their HTTP-01 solver — that is the only line changed from
5.2's file. **Always start with staging**, which `gateway.yml` does: its
certificates are signed by an untrusted root, but its rate limits are loose,
whereas production enforces
[limits](https://letsencrypt.org/docs/rate-limits/) that are easy to burn
through while a DNS record or a firewall rule is still wrong.

The issuers have no work to do yet, so they are ready immediately:

```shell
kubectl get clusterissuer
kubectl describe clusterissuer letsencrypt-staging
```

## 7. Deploy the demo

```shell
kubectl apply \
  -f deployment.yml \
  -f service.yml \
  -f gateway.yml \
  -f http-route.yml \
  -f http-redirect-route.yml \
  -n snippet-backend-letsencrypt-demo
```

Wait for the image to be pulled from GHCR and the readiness probe to pass:

```shell
kubectl rollout status deployment/my-deployment -n snippet-backend-letsencrypt-demo
```

Then wait for the Gateway's `ADDRESS` column to be populated (`Ctrl+C` to stop
watching):

```shell
kubectl get gateway -n snippet-backend-letsencrypt-demo --watch
```

`PROGRAMMED` will read `False` at this stage, and that is expected: the HTTPS
listener points at a Secret that does not exist yet. `kubectl describe` spells
it out, per listener — `ResolvedRefs: False`, *"Secret ... does not exist"* on
`https`, while `http` is fine and already serving:

```shell
kubectl describe gateway my-gateway -n snippet-backend-letsencrypt-demo
```

That half-working state is the whole point. The `http` listener is what
carries the ACME challenge, and it is up before any certificate exists.

While you are here, check the two hops the route depends on — the Service must
have an endpoint, and the HTTPRoute must have been accepted and have resolved
its backend:

```shell
kubectl get endpointslices -l kubernetes.io/service-name=my-service \
  -n snippet-backend-letsencrypt-demo
kubectl describe httproute my-route -n snippet-backend-letsencrypt-demo
```

Look for `Accepted: True` and `ResolvedRefs: True` under `Parents`.

### Point DNS at the Gateway

```shell
GATEWAY_IP=$(kubectl get gateway my-gateway -n snippet-backend-letsencrypt-demo \
  -o jsonpath='{.status.addresses[0].value}')
echo $GATEWAY_IP
```

Create an `A` record for your domain pointing at it (or a `CNAME` if your
provider hands out a hostname rather than an IP), then wait for it to
propagate. Do not skip this check — a stale record is the single most common
cause of a failing challenge:

```shell
dig +short my-app.example.com
curl -i http://my-app.example.com/
```

The `curl` should answer `301` towards `https://`, proving the `http`
listener is reachable from the outside on port 80.

## 8. Watch the certificate being issued

cert-manager reacts to the annotation as soon as the Gateway exists, and the
Certificate goes `READY=True` a minute or two after DNS resolves correctly:

```shell
kubectl get certificate -n snippet-backend-letsencrypt-demo --watch
```

This is the object nobody wrote: it was generated by the gateway-shim from the
listener, and is named after the Secret:

```shell
kubectl get certificate my-tls -n snippet-backend-letsencrypt-demo -o yaml
```

Watch the whole chain while it works — the intermediate objects, and the
temporary solver Pod, Service and HTTPRoute named `cm-acme-http-solver-xxxxx`,
appear and disappear within a couple of minutes:

```shell
kubectl get certificate,certificaterequest,order,challenge -n snippet-backend-letsencrypt-demo
kubectl get pods,svc,httproute -n snippet-backend-letsencrypt-demo
```

`kubectl describe challenge` is the single most useful command when this
hangs: its status message is the verbatim answer Let's Encrypt got when it
fetched the token:

```shell
kubectl describe challenge -n snippet-backend-letsencrypt-demo
```

Once `READY` is `True`, the Secret exists — an ordinary `kubernetes.io/tls`
Secret, holding `tls.crt` and `tls.key`. Note that the namespace now contains
**two** Secrets of two different kinds: `ghcr-secret`, which you created to
*pull* the image, and `my-tls`, which cert-manager created to *serve* it:

```shell
kubectl get secret -n snippet-backend-letsencrypt-demo
```

Read the certificate back out of the cluster. Note the issuer: `(STAGING)`
something, from Let's Encrypt's test hierarchy, and a validity of 90 days:

```shell
kubectl get secret my-tls -n snippet-backend-letsencrypt-demo \
  -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -subject -issuer -dates
```

The Gateway should now be fully programmed:

```shell
kubectl get gateway -n snippet-backend-letsencrypt-demo
```

## 9. Test it, with the staging certificate

```shell
curl https://my-app.example.com/
```

```
curl: (60) SSL certificate problem: unable to get local issuer certificate
```

Expected: the certificate is signed by a real CA hierarchy, it is simply
Let's Encrypt's **staging** one, which no client trusts. `-k` shows the app,
and confirms everything but the trust chain works:

```shell
curl -k https://my-app.example.com/
```

```json
{"message":"hello"}
```

FastAPI's generated documentation comes through the same route:

```shell
curl -k https://my-app.example.com/openapi.json
```

Look at what the Gateway serves — the issuer name is the interesting line:

```shell
openssl s_client -connect my-app.example.com:443 -servername my-app.example.com </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates
```

And check the redirect on port 80, which now that the challenge is over
catches everything:

```shell
curl -I http://my-app.example.com/
```

## 10. Switch to the production issuer

Only once the above works end to end. Point the annotation at the real
Let's Encrypt:

```shell
sed -i 's|cert-manager.io/cluster-issuer: letsencrypt-staging|cert-manager.io/cluster-issuer: letsencrypt|' gateway.yml
kubectl apply -f gateway.yml -n snippet-backend-letsencrypt-demo
```

cert-manager notices the `issuerRef` of the Certificate no longer matches and
re-issues it, through the same challenge:

```shell
kubectl get certificate -n snippet-backend-letsencrypt-demo --watch
```

The issuer is now one of Let's Encrypt's production intermediates:

```shell
kubectl get secret my-tls -n snippet-backend-letsencrypt-demo \
  -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -subject -issuer -dates
```

And plain `curl`, with no flag at all, finally works:

```shell
curl https://my-app.example.com/
```

```json
{"message":"hello"}
```

Open `https://my-app.example.com/docs` in a browser: the Swagger UI of your
own app, behind a real padlock, with no warning and nothing to add to any
trust store. That is the end point the whole series was heading towards.

## Nothing left to do

The certificate expires in 90 days and cert-manager will replace it around day
60, on its own, in place. Envoy Gateway watches the Secret and reloads the
proxy — no restart, no downtime, and nothing to do in the app:

```shell
kubectl get certificate my-tls -n snippet-backend-letsencrypt-demo \
  -o jsonpath='{.status.notBefore} -> {.status.notAfter} (renew at {.status.renewalTime}){"\n"}'
```

To rehearse a renewal instead of waiting two months, force one (mind the
rate limits if you do it repeatedly):

```shell
cmctl renew my-tls -n snippet-backend-letsencrypt-demo
```

## Scaling and updating

Unchanged from 6.2.2 — neither the Gateway, nor the routes, nor the
certificate is touched by any of it. The certificate belongs to the Gateway,
so replicas and image tags come and go underneath it:

```shell
kubectl scale deployment/my-deployment --replicas=3 -n snippet-backend-letsencrypt-demo
for i in $(seq 6); do curl -s https://my-app.example.com/ > /dev/null; done
kubectl logs -l app=my-app --prefix --tail=3 -n snippet-backend-letsencrypt-demo
```

```shell
podman build -t ghcr.io/jeremiedecock/hello-fastapi:1.0.1 .
podman push ghcr.io/jeremiedecock/hello-fastapi:1.0.1
kubectl set image deployment/my-deployment \
  my-container=ghcr.io/jeremiedecock/hello-fastapi:1.0.1 \
  -n snippet-backend-letsencrypt-demo
kubectl rollout status deployment/my-deployment -n snippet-backend-letsencrypt-demo
```

`my-container=` is the **container** name from `deployment.yml`, and the new
tag matters: overwriting `1.0` would change what every other demo in the
series pulls. `kubectl rollout undo deployment/my-deployment` reverts. Scale
back down before moving on:

```shell
kubectl scale deployment/my-deployment --replicas=1 -n snippet-backend-letsencrypt-demo
```

## When it does not work

Two chains to walk, and the symptom tells you which. **A TLS error, or no
certificate at all** is the cert-manager chain; **a `404`, a `503` or a
`ImagePullBackOff`** is the routing chain from 6.2.2, which HTTPS did not
change.

### The certificate chain

Each object's `status` names the next one to look at:

```shell
kubectl describe gateway my-gateway -n snippet-backend-letsencrypt-demo
kubectl describe certificate my-tls -n snippet-backend-letsencrypt-demo
kubectl describe certificaterequest -n snippet-backend-letsencrypt-demo
kubectl describe order -n snippet-backend-letsencrypt-demo
kubectl describe challenge -n snippet-backend-letsencrypt-demo
kubectl logs -n cert-manager deployment/cert-manager --tail=100
```

- **No Certificate object is ever created.** The Gateway API integration is
  off (`config.gatewayAPI.enabled`), or cert-manager started before the
  Gateway API CRDs existed — restart it. Otherwise the listener is not
  eligible: it needs a non-empty `hostname`, `mode: Terminate` and a
  `certificateRefs[].name`.
- **The Challenge stays `pending`, with a 404 or a timeout in its message.**
  Whatever Let's Encrypt saw is in that message. Either DNS does not point at
  the Gateway, or port 80 is blocked upstream, or the `http` listener is gone.
  Reproduce what the ACME server does, from outside the cluster:
  `curl http://my-app.example.com/.well-known/acme-challenge/test`.
- **The Challenge fails with a rate-limit error.** You were on the production
  issuer too early. Switch back to staging, fix the problem there, and note
  that the duplicate-certificate limit takes a week to clear.
- **The Gateway stays `PROGRAMMED=False` while the Certificate is `True`.**
  Mismatched names: the Secret written by cert-manager and the one in
  `certificateRefs` must be the same, in the Gateway's namespace.

### The routing chain

```shell
kubectl describe httproute my-route -n snippet-backend-letsencrypt-demo
kubectl get endpointslices -l kubernetes.io/service-name=my-service -n snippet-backend-letsencrypt-demo
kubectl describe pod -l app=my-app -n snippet-backend-letsencrypt-demo | tail -20
```

- **`404` from Envoy.** The request reached the proxy and matched no route.
  Either the hostname you queried is not the one in `hostnames:`, or the
  `sectionName` does not name an existing listener — both routes name one
  here, unlike 6.2.2's, and a typo there means `Accepted: False` with
  `NoMatchingParent`.
- **`503`.** The route matched, the backend has nothing behind it.
  `ResolvedRefs: False` / `BackendNotFound` means a wrong Service name or
  port in `backendRefs` (`80` here, not `8000`); a resolved ref with an empty
  `endpointslices` listing means no Pod is ready.
- **Pods in `ImagePullBackOff` / `ErrImagePull`.** The registry side, as in
  6.1. A `401` in the Pod events means the Secret is missing, misnamed in
  `imagePullSecrets`, **in another namespace**, or built with a
  `--docker-server` other than exactly `ghcr.io`.
- **Pods `Running` but `0/1 READY`.** The readiness probe is failing;
  `kubectl describe pod -l app=my-app` gives the status code it got. Note that
  this has nothing to do with TLS: the probe never goes through the Gateway.
- **Pods `CrashLoopBackOff`.** Not Kubernetes: `kubectl logs -l app=my-app`
  has the app's traceback.

## Remove the demo

```shell
kubectl delete \
  -f http-redirect-route.yml \
  -f http-route.yml \
  -f gateway.yml \
  -f service.yml \
  -f deployment.yml \
  -n snippet-backend-letsencrypt-demo

kubectl delete namespace snippet-backend-letsencrypt-demo
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
deleting a CRD garbage-collects every object of that kind — every Certificate,
Issuer and ClusterIssuer on the cluster. Remove them by hand, knowingly, only
if nothing else uses cert-manager:

```shell
kubectl get crd -o name | grep cert-manager.io
```

**Keep the image.** `hello-fastapi:1.0` is this app — `{"message": "hello"}`,
documentation enabled — and 6.4 expects exactly that content behind the tag.

When you are done with the series, revoke the PAT from *Settings → Developer
settings → Personal access tokens* and clear the local credentials with
`podman logout ghcr.io`.
