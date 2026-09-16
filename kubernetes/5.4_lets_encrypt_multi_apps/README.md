# HTTPS for several apps behind one Gateway (Let's Encrypt + cert-manager)

This example is the meeting point of two earlier ones, and assumes both have
been read:

- [`4.3.2_gateway_api_envoy_gateway_multi_apps`](../4.3.2_gateway_api_envoy_gateway_multi_apps/)
  — two applications, each in its own namespace, sharing one Gateway and
  routed by hostname, over plain HTTP;
- [`5.2_lets_encrypt`](../5.2_lets_encrypt/) — a single application served
  over HTTPS, with a Let's Encrypt certificate obtained and renewed by
  [cert-manager](https://cert-manager.io/).

Here, **two applications are served over HTTPS under two different domain
names, behind a single public IP address**, each with **its own certificate**.

Nothing conceptual is new: the Gateway API, the ACME HTTP-01 challenge, the
gateway-shim, the cross-namespace route attachment are all explained in those
two examples, and this README does not repeat them. It only covers what
changes when the two are combined.

## What changes

| | `4.3.2` | `5.2` | `5.4` (here) |
| --- | --- | --- | --- |
| Applications | 2 | 1 | 2 |
| Namespaces | 3, hardcoded | 1, on the command line | 3, hardcoded |
| Listeners | 1 (`HTTP:80`) | 2 (`HTTP:80`, `HTTPS:443`) | **4** (one HTTP + one HTTPS per hostname) |
| Certificates | none | 1 | **2**, one per hostname |
| ClusterIssuers | — | 2 (staging + production) | 2, **unchanged** |
| HTTPRoutes | 2 | 2 | 4 (one app route + one redirect per application) |
| `sectionName` on routes | optional | recommended | **mandatory** |
| DNS records | none | 1 `A` | 2 `A`, **same IP** |

## Layout

One directory per namespace, every manifest hardcoding its
`metadata.namespace`, as in 4.3.2:

```
gateway-class/gateway-class.yml   # cluster-wide, belongs to no namespace
gateway/                          # namespace snippet-letsencrypt-multi-demo-gateway
├── namespace.yml
├── cluster-issuer.yml            # cluster-wide too (see below)
└── gateway.yml
app1/                             # namespace snippet-letsencrypt-multi-demo-app1
├── namespace.yml
├── deployment.yml
├── service.yml
├── http-route.yml
└── http-redirect-route.yml
app2/                             # namespace snippet-letsencrypt-multi-demo-app2
└── ... identical
```

The two applications are again deliberately identical (a stock nginx server),
so that the only thing this example demonstrates is the certificate handling:

| Hostname | Namespace | Listeners | Certificate / Secret |
| --- | --- | --- | --- |
| `app1.example.com` | `snippet-letsencrypt-multi-demo-app1` | `http-app1`, `https-app1` | `app1-tls` |
| `app2.example.com` | `snippet-letsencrypt-multi-demo-app2` | `http-app2`, `https-app2` | `app2-tls` |

`cluster-issuer.yml` sits in `gateway/` because its HTTP-01 solver names this
demo's Gateway, but the two ClusterIssuers it declares are **cluster-scoped**:
like the GatewayClass, they survive the deletion of the namespace and have to
be removed explicitly.

## One certificate per hostname

A single public IP means a single load balancer, hence a **single Gateway**
— it is the Gateway that owns the address. Everything else follows from its
listeners.

The gateway-shim creates **one `Certificate` per eligible HTTPS listener**,
named after the Secret that listener asks for. Two HTTPS listeners, two
hostnames, two Secrets: two certificates, each covering a single name. The
annotation on the Gateway is still one line, and still the entire trigger.

This is not the only possible split, and the other two are worth knowing:

| Approach | How | Trade-off |
| --- | --- | --- |
| **Two certificates** (used here) | the annotation, two HTTPS listeners | Independent: a broken DNS record for `app2` does not stop `app1` from being issued or renewed. Simplest, and the default. |
| **One certificate, two SANs** | write the `Certificate` by hand, `dnsNames: [app1…, app2…]`, one Secret referenced by both listeners | A single ACME order; but renewal is all-or-nothing, adding a third name re-issues everything, and the full list of names is visible in the certificate. |
| **One wildcard, `*.example.com`** | **DNS-01 only** — HTTP-01 never issues wildcards | Covers every present and future subdomain, and needs neither port 80 nor a public IP; at the price of API credentials for the DNS zone and a provider-specific webhook. |

Two certificates for two applications is the right default. A wildcard starts
paying off somewhere around five to ten subdomains, or when port 80 cannot be
opened.

## The Gateway: four listeners

Several listeners may share a port, provided their `hostname` values differ
and their `name` values are unique. On 443 the Envoy proxy picks the
certificate by **SNI**, on 80 the route by the `Host` header:

```yaml
listeners:
  - name: http-app1     # HTTP  :80   hostname app1.example.com
  - name: https-app1    # HTTPS :443  hostname app1.example.com  -> Secret app1-tls
  - name: http-app2     # HTTP  :80   hostname app2.example.com
  - name: https-app2    # HTTPS :443  hostname app2.example.com  -> Secret app2-tls
```

Two consequences for the routes:

- `sectionName` is now **mandatory** in every `parentRefs`. With four
  listeners, omitting it attaches the route to every listener whose hostname
  is compatible — including the HTTP one, which would defeat the redirect.
- each application owns **two** HTTPRoutes: the real one on its HTTPS
  listener, and the 301 redirect on its HTTP listener. Both live in the
  application's namespace, next to what they expose.

> **On the HTTP listeners.** A single listener on port 80 with *no* hostname
> would serve both applications' redirects and both ACME challenges just as
> well, and cert-manager would ignore it either way — it only looks at HTTPS
> listeners. Four listeners are used here because the symmetry makes the
> ownership obvious: everything about `app1.example.com` is named after it.
> Three listeners are a perfectly valid, shorter alternative.

## Where the certificates live

The Certificates and their Secrets are created in the **Gateway's namespace**,
not in the applications': the gateway-shim does not support cross-namespace
`certificateRefs`, and neither does the Gateway API.

That constraint matches the role split the Gateway API is built around, and
which 4.3.2 describes: the cluster operator owns the Gateway, its listeners,
and now its certificates; each application team owns only its own HTTPRoutes,
in its own namespace. An application team never sees the private keys of the
certificate that fronts it.

## The ACME challenge, twice

The two challenges run **in parallel and independently**: two `Certificate`s,
two `Order`s, two `Challenge`s, and two sets of temporary solver objects (Pod,
Service and HTTPRoute) — all of them in the Gateway's namespace, since that is
where the Certificates are.

One subtlety, and the only real trap of this example: the issuer's
`solvers[].http01.gatewayHTTPRoute.parentRefs` **must not carry a
`sectionName`**. That single parentRef is reused for every challenge of every
domain, so pinning it to one listener would send the `app2` challenge to a
listener whose hostname is `app1.example.com`; the hostnames would not
intersect, the solver route would not attach, and the challenge would time out
with a 404. Left unset, each solver HTTPRoute attaches to whichever listeners
match its own hostname, which is exactly what is wanted.

The listeners' `allowedRoutes` must of course accept the solver routes too,
but this comes for free: they are created in the Gateway's own namespace, so
even `from: Same` would work. The `from: All` used here is what the two
*application* namespaces need.

## Prerequisites

Same as 5.2, with one DNS record per application:

- **Envoy Gateway and the `eg` GatewayClass** — see
  [4.3.1](../4.3.1_gateway_api_envoy_gateway/README.md#prerequisite-a-gateway-api-implementation),
  including the checks to make before installing anything cluster-wide;
- **cert-manager, with its Gateway API integration enabled** — see
  [5.2](../5.2_lets_encrypt/README.md#installing-cert-manager). The
  `config.gatewayAPI.enabled=true` setting is the one that is off by default
  and silently does nothing when forgotten;
- **a cluster whose Gateway gets a public IP**, reachable from the internet on
  ports 80 and 443;
- **two domain names you own**, pointing at that address (created a few steps
  below, once the address exists).

Replace the example domains with your own, and the contact address in the
issuers:

```shell
sed -i 's/app1\.example\.com/app1.your-domain.com/g' gateway/gateway.yml app1/*.yml
sed -i 's/app2\.example\.com/app2.your-domain.com/g' gateway/gateway.yml app2/*.yml
sed -i 's/you@example\.com/your-address@your-domain.com/g' gateway/cluster-issuer.yml
```

## Deploy the demo

The GatewayClass first, unless one already exists (see 4.3.1):

```shell
kubectl apply -f gateway-class/gateway-class.yml
```

Then the Gateway namespace, the issuers and the Gateway. The issuers are
applied before the Gateway so that the Certificates the annotation triggers
find their `issuerRef` right away:

```shell
kubectl apply \
  -f gateway/namespace.yml \
  -f gateway/cluster-issuer.yml \
  -f gateway/gateway.yml
```

```shell
kubectl get clusterissuer
```

Wait for the Gateway's `ADDRESS` column to be populated (`Ctrl+C` to stop
watching). `PROGRAMMED` stays `False`, as in 5.2 — now because *two*
listeners point at Secrets that do not exist yet:

```shell
kubectl get gateway -n snippet-letsencrypt-multi-demo-gateway --watch
```

`describe` reports the state listener by listener, which is the view that
matters from here on — `http-app1` and `http-app2` are already serving, while
the two HTTPS ones are unresolved:

```shell
kubectl describe gateway my-gateway -n snippet-letsencrypt-multi-demo-gateway
```

### Point both domains at the Gateway

```shell
GATEWAY_IP=$(kubectl get gateway my-gateway -n snippet-letsencrypt-multi-demo-gateway -o jsonpath='{.status.addresses[0].value}')
echo $GATEWAY_IP
```

Create **two** `A` records, `app1` and `app2`, both pointing at that same
address (or two `CNAME`s if your provider hands out a hostname), then check
that both resolve before going further:

```shell
dig +short app1.example.com
dig +short app2.example.com
```

### Deploy the two applications

```shell
kubectl apply \
  -f app1/namespace.yml \
  -f app1/deployment.yml \
  -f app1/service.yml \
  -f app1/http-route.yml \
  -f app1/http-redirect-route.yml
```

```shell
kubectl apply \
  -f app2/namespace.yml \
  -f app2/deployment.yml \
  -f app2/service.yml \
  -f app2/http-route.yml \
  -f app2/http-redirect-route.yml
```

Check that the four routes were accepted by the Gateway, and that each landed
on the listener it asked for — a wrong or missing `sectionName` shows up here:

```shell
kubectl describe httproute -n snippet-letsencrypt-multi-demo-app1
kubectl describe httproute -n snippet-letsencrypt-multi-demo-app2
```

Both redirects should already answer on port 80, before any certificate
exists:

```shell
curl -I http://app1.example.com/
curl -I http://app2.example.com/
```

## Watch the two certificates being issued

Everything happens in the Gateway's namespace. Two Certificates appear, named
after the Secrets of the two HTTPS listeners, and go `READY=True` a minute or
two after DNS resolves correctly:

```shell
kubectl get certificate -n snippet-letsencrypt-multi-demo-gateway --watch
```

The whole chain, doubled — two Orders, two Challenges, running at the same
time:

```shell
kubectl get certificate,certificaterequest,order,challenge -n snippet-letsencrypt-multi-demo-gateway
```

And the temporary solver objects, two of each, for the couple of minutes the
challenges last:

```shell
kubectl get pods,svc,httproute -n snippet-letsencrypt-multi-demo-gateway
```

Note that the two are genuinely independent: if only one hostname is wrong,
one Certificate goes `READY=True` and the other keeps retrying. The Gateway as
a whole stays `PROGRAMMED=False` until both are there, but the working
hostname is served over HTTPS in the meantime.

Once both are ready, both Secrets exist, and the Gateway is fully programmed:

```shell
kubectl get secret app1-tls app2-tls -n snippet-letsencrypt-multi-demo-gateway
kubectl get gateway -n snippet-letsencrypt-multi-demo-gateway
```

Read the two certificates back, and check that each carries its own single
name — the `Subject` line is the interesting one:

```shell
for name in app1 app2; do
  kubectl get secret $name-tls -n snippet-letsencrypt-multi-demo-gateway \
    -o jsonpath='{.data.tls\.crt}' | base64 -d \
    | openssl x509 -noout -subject -issuer -dates
done
```

## Test it, with the staging certificates

Both fail to verify, for the reason given in 5.2: the staging hierarchy is not
trusted by anything. `-k` shows the nginx page of each application:

```shell
curl -k https://app1.example.com/
curl -k https://app2.example.com/
```

The interesting check is that the Gateway really serves a *different*
certificate per name, selected by SNI on the same IP and the same port:

```shell
for name in app1 app2; do
  openssl s_client -connect $name.example.com:443 -servername $name.example.com </dev/null 2>/dev/null \
    | openssl x509 -noout -subject
done
```

Both commands open a connection to the same IP and the same port; the only
difference is the name announced by the client before the handshake, and that
is all SNI is. It is also why a single IP can serve any number of certificates,
and why a client too old to send SNI cannot be served correctly here.

## Switch to the production issuer

Only once the above works end to end for **both** hostnames. Changing the one
annotation re-issues **both** certificates:

```shell
sed -i 's|cert-manager.io/cluster-issuer: letsencrypt-staging|cert-manager.io/cluster-issuer: letsencrypt|' gateway/gateway.yml
kubectl apply -f gateway/gateway.yml
```

```shell
kubectl get certificate,order,challenge -n snippet-letsencrypt-multi-demo-gateway
```

```shell
kubectl get certificate -n snippet-letsencrypt-multi-demo-gateway --watch
```

Then plain `curl`, with no flag, on both:

```shell
curl https://app1.example.com/
curl https://app2.example.com/
```

Both open in a browser with a real padlock, on a single public IP address.
Renewal is the non-event described in 5.2, twice: cert-manager renews each
certificate around day 60 of its 90, in place, and Envoy Gateway reloads.

## Let's Encrypt limits with several hostnames

Two hostnames do not come close to any production limit, but the counters are
worth knowing before this pattern grows to ten applications
([official reference](https://letsencrypt.org/docs/rate-limits/), which does
move — Let's Encrypt revised several of these in 2025):

| Limit | Value | Effect here |
| --- | --- | --- |
| Certificates per **registered domain** | 50 / week, sliding | `example.com` counts for *all* its subdomains together. This is the shared counter to watch as the number of applications grows. |
| **Duplicate certificates** (same exact set of names) | **5 / week** | The one that hurts, and that cannot be raised. It is counted **per set of names**, so `app1` and `app2` each get their own 5. Repeated `cmctl renew` or Secret deletions burn it fast. |
| Failed validations | 5 / hour / hostname | **Per hostname** too: a misconfigured `app2` does not lock `app1` out. |
| Names per certificate | 100 | Only relevant to the "one certificate, many SANs" variant. |

Renewals (the same set of names as an already-issued certificate) are exempt
from the per-registered-domain limit, but **not** from the duplicate limit.
Two more things to keep in mind on a real domain: a `CAA` record on the zone
must allow `letsencrypt.org`, and every issued name is published in the public
Certificate Transparency logs — one more small argument for separate
certificates over a shared multi-SAN one.

Staging limits are far looser, which is the whole reason to start there.

## When it does not work

Everything in 5.2's troubleshooting section applies, with one addition: **look
per hostname, and in the right namespace**. The Certificates, Orders,
Challenges and solver Pods are in `snippet-letsencrypt-multi-demo-gateway`,
the HTTPRoutes in the application namespaces.

```shell
kubectl describe gateway my-gateway -n snippet-letsencrypt-multi-demo-gateway
kubectl describe certificate -n snippet-letsencrypt-multi-demo-gateway
kubectl describe challenge -n snippet-letsencrypt-multi-demo-gateway
kubectl logs -n cert-manager deployment/cert-manager --tail=100
```

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
  instead of the `https-*` one is accepted, and then shadowed by the redirect.
- **The Gateway stays `PROGRAMMED=False` with one Certificate ready.** Normal
  while the other one is missing. `describe` the Gateway and read the
  per-listener conditions rather than the top-level one.

## Adding a third application

Nothing cluster-wide changes: copy `app2/` to `app3/` with its own namespace
and hostname, add two listeners to the Gateway, add one DNS record. The
annotation, the issuers and cert-manager are untouched — the third certificate
appears on its own.

## Remove the demo

The three namespaces take the applications, the Gateway, both Certificates and
both Secrets with them:

```shell
kubectl delete namespace \
  snippet-letsencrypt-multi-demo-app1 \
  snippet-letsencrypt-multi-demo-app2 \
  snippet-letsencrypt-multi-demo-gateway
```

Remove the two DNS records too.

The ClusterIssuers are cluster-scoped and survive their directory's namespace.
They are only useful to this demo — their solver names its Gateway — but check
that nobody else adopted them first:

```shell
kubectl get certificate --all-namespaces \
  -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,ISSUER:.spec.issuerRef.name'
kubectl delete -f gateway/cluster-issuer.yml
```

The ACME account keys stay behind in cert-manager's namespace; keeping them is
harmless and saves re-registering:

```shell
kubectl delete secret letsencrypt-staging-account-key letsencrypt-account-key -n cert-manager
```

### Shared cluster add-ons: stop and check first

cert-manager, the Envoy Gateway controller and the GatewayClass are
cluster-wide and shared. **Do not delete them if you did not install them, or
if anything else on the cluster still uses them.** The checks, and the warning
about deleting cert-manager's CRDs, are in
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
