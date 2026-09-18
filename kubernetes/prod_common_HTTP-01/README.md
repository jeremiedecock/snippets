# `prod_common_HTTP-01` — shared cluster infrastructure, HTTP-01 flavour

Installed **once per cluster**. Provides the single public entry point that
every application built from [`../prod_app`](../prod_app/) attaches to.

Certificates are proven by the **HTTP-01** challenge: no DNS credentials and
no extra server to run, at the price of one certificate — and therefore one
Gateway listener — **per application**.

> The alternative is [`../prod_common_DNS-01`](../prod_common_DNS-01/): one
> wildcard certificate, no Gateway change when an application is added, but a
> self-hosted acme-dns server and a DNS delegation to set up. Pick one; they
> are mutually exclusive on a cluster (both define `gateway-infra` and the
> same ClusterIssuer names).

| | `HTTP-01` (here) | `DNS-01` |
| --- | --- | --- |
| Extra infrastructure | none | acme-dns (Deployment, PVC, public IP on UDP/TCP 53) |
| DNS work, once | — | delegation `A` + `NS`, one `CNAME` |
| Port 80 open to the internet | **required** | not required |
| Certificates | one per application | **one wildcard for all** |
| Adding an application | **edit the Gateway** (one listener) + `A` record | `A` record only |
| Wildcard certificates | impossible | yes |
| `sectionName` in app routes | `https-<app>` | `https` |
| Let's Encrypt counters | one issuance per app | one, shared |

| Object | Name | Namespace |
| --- | --- | --- |
| GatewayClass | `envoy` | cluster-wide |
| Gateway | `gateway-infra` | `gateway-infra` |
| HTTPRoute (301 http→https, all hosts) | `https-redirect` | `gateway-infra` |
| Certificate / Secret, per application | `<app>-tls` | `gateway-infra` |
| ClusterIssuers | `letsencrypt-staging`, `letsencrypt` | cluster-wide |

```
gateway-class.yml               GatewayClass (cluster-wide)
gateway/
├── namespace.yml
├── gateway.yml                 one hostname-less http listener + one https listener per app
└── http-redirect-route.yml     301 for every hostname
cert-manager/cluster-issuer.yml Let's Encrypt staging + production, HTTP-01
justfile
```

## Prerequisites

- a Kubernetes cluster whose LoadBalancer Services get a **public IP**,
  reachable from the internet on **ports 80 and 443** — port 80 carries the
  ACME challenge, so it cannot be closed;
- `kubectl`, `helm`, `just`, `openssl`;
- a **domain you own**, with one `A` record per application (or a single
  wildcard `A` record covering them all).

## Install

```shell
just configure example.com ops@example.com
just check        # what is already installed -- read before going further
just install      # Envoy Gateway + cert-manager + GatewayClass
just deploy       # issuers + Gateway + redirect route, then watches
just gateway-ip
```

`just install` enables `config.gatewayAPI.enabled=true` on cert-manager,
which is off by default and silently does nothing when forgotten, then
restarts cert-manager (it reads the Gateway API CRDs only at startup).

At this point the Gateway has a single `http` listener, is `PROGRAMMED=True`,
and answers a 301 on every hostname. It holds no certificate yet: there is
nothing to certify until the first application is onboarded.

## Onboarding an application

Four steps, in this order.

**1. The `A` record.** `invoices.example.com` → the Gateway IP. The ACME
server resolves the name itself, so this must be live before the challenge
runs. A wildcard `A` record on the zone covers every future application.

**2. The listener.** One per application:

```shell
just listener invoices invoices.example.com   # prints the block to paste
# paste it under spec.listeners in gateway/gateway.yml
kubectl apply -f gateway/gateway.yml
just certificate-watch                        # READY=True after a minute or two
```

`PROGRAMMED` goes `False` while the new listener waits for its Secret, and
back to `True` once cert-manager writes it. Applications already served are
unaffected: an unresolved listener does not take the others down.

**3. The namespace grant.**

```shell
just grant invoices     # labels the namespace gateway-access=true
just tenants
```

**4. The application**, from [`../prod_app`](../prod_app/) — answering
`https-invoices` to the `gateway_listener` question, since each application
has its own listener here.

## Switch to production

Only once one application works end to end on staging. **This re-issues every
certificate at once**, so do it early, while there is only one:

```shell
just use-production
just certificate-show invoices
```

## Day to day

```shell
just status               # gateway, routes, certificates, all tenants
just describe             # per-listener conditions -- read when PROGRAMMED=False
just certificates         # certificate, request, order, challenge
just certificate-show invoices
just logs-cert-manager
```

| Symptom | Look at |
| --- | --- |
| `PROGRAMMED=False` | `just describe` — one listener waiting for its Secret is enough, and is normal right after `just listener` |
| Challenge times out with a 404 | the `A` record for *that* hostname, then `curl http://<host>/.well-known/acme-challenge/test`; port 80 must be open |
| Solver route reports `NoMatchingListenerHostname` | someone gave the `http` listener a hostname, or changed the issuer's `sectionName` — see the comment in `cluster-issuer.yml` |
| An app's route is `Accepted=False` | its namespace lacks `gateway-access=true` (`just grant <ns>`), or its `sectionName` is `https` instead of `https-<app>` |
| `404` from Envoy for a hostname | no listener for it, no `A` record, or no HTTPRoute matches |
| Certificate stuck `READY=False` | `just certificates`, then `kubectl describe challenge -n gateway-infra`; its message is the verbatim CA answer |

## Operating notes

- **Rate limits** matter more here than with a wildcard, because every
  application issues its own certificate
  ([reference](https://letsencrypt.org/docs/rate-limits/)): 50 certificates
  per week and per *registered domain* — the counter shared by all your
  subdomains — and 5 duplicates per week for an identical set of names, which
  is the one that hurts. Staging limits are far looser; stay there while
  onboarding.
- **Failed validations are counted per hostname**, so a misconfigured
  application does not lock the others out.
- **Renewal** is automatic at ~day 60 of 90, through the same challenge. Port
  80 must still be open then — this is the usual cause of a renewal failing
  months after a working install.
- **Beyond ~10 applications**, the per-application listener becomes the
  chore this directory is trading against, and
  [`../prod_common_DNS-01`](../prod_common_DNS-01/) starts paying off.
- **Upgrades.** Bump `envoy_gateway_version` / `cert_manager_version` in the
  justfile and `helm upgrade`; read the Envoy Gateway release notes first, a
  Gateway API version bump can require re-applying CRDs.

## Uninstall

Destroys the entry point of every application on the cluster. Check first:

```shell
kubectl get httproute --all-namespaces
kubectl get certificate,issuer --all-namespaces
```

```shell
kubectl delete -f gateway/ -f cert-manager/cluster-issuer.yml
kubectl delete -f gateway-class.yml
helm uninstall cert-manager -n cert-manager
helm uninstall eg -n envoy-gateway-system
```

`eg` is the Helm *release* name, unrelated to the GatewayClass name.
`helm uninstall` leaves cert-manager's CRDs in place on purpose: deleting a
CRD garbage-collects every object of that kind cluster-wide.
