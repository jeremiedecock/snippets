# `prod_common_DNS-01` — shared cluster infrastructure, DNS-01 flavour

Installed **once per cluster**. Provides the single public entry point that
every application built from [`../prod_app`](../prod_app/) attaches to.

Certificates are proven by the **DNS-01** challenge against a self-hosted
[acme-dns](https://github.com/joohoi/acme-dns) server, which buys **one
wildcard certificate for every application**.

> The alternative is [`../prod_common_HTTP-01`](../prod_common_HTTP-01/): no
> extra server and no DNS delegation, at the price of one certificate and one
> Gateway listener per application. Pick one; they are mutually exclusive on
> a cluster (both define `gateway-infra` and the same ClusterIssuer names).

| | `DNS-01` (here) | `HTTP-01` |
| --- | --- | --- |
| Extra infrastructure | acme-dns (Deployment, PVC, public IP on UDP/TCP 53) | none |
| DNS work, once | delegation `A` + `NS`, one `CNAME` | — |
| Port 80 open to the internet | not required | **required** |
| Certificates | **one wildcard for all** | one per application |
| Adding an application | `A` record only | edit the Gateway (one listener) + `A` record |
| Wildcard certificates | yes | impossible |
| `sectionName` in app routes | `https` | `https-<app>` |
| Let's Encrypt counters | one, shared | one issuance per app |


| Object | Name | Namespace |
| --- | --- | --- |
| GatewayClass | `envoy` | cluster-wide |
| Gateway | `gateway-infra` | `gateway-infra` |
| HTTPRoute (301 http→https, all hosts) | `https-redirect` | `gateway-infra` |
| Wildcard certificate / Secret | `wildcard-tls` (`*.example.com`) | `gateway-infra` |
| ClusterIssuers | `letsencrypt-staging`, `letsencrypt` | cluster-wide |
| acme-dns (DNS-01 solver) | `acme-dns` | `acme-dns` |

**Adding an application never modifies this directory.** One wildcard
certificate covers every subdomain, and the shared redirect covers every
hostname; a new app needs an `A` record, a namespace label, and its own
HTTPRoute.

```
gateway-class.yml               GatewayClass (cluster-wide)
gateway/
├── namespace.yml
├── gateway.yml                 listeners http + https, hostname *.example.com
└── http-redirect-route.yml     301 for every hostname
cert-manager/cluster-issuer.yml Let's Encrypt staging + production, DNS-01
acme-dns/                       self-hosted DNS-01 solver (6 manifests)
optional/                       extra domain outside the wildcard, apex certificate
justfile
```

## Prerequisites

- a Kubernetes cluster whose LoadBalancer Services get **public IPs**;
- `kubectl`, `helm`, `just`, `jq`, `dig`, `openssl`;
- a **domain you own** (`example.com` below) and the ability to create `A`,
  `NS` and `CNAME` records in its zone;
- **one stable public IP reachable on UDP and TCP port 53** for acme-dns.
  UDP/53 is the port most often blocked by a provider firewall. acme-dns does
  not have to run in this cluster — a small VPS is a fine, arguably better
  home for it, shared by every cluster you own.

## Install

### 0. Configure

Replaces every placeholder in every manifest. Run once, then commit.

```shell
just configure example.com ops@example.com auth.example.com
```

The third argument is the zone delegated to acme-dns. It must be a subdomain
you are willing to hand over entirely (nothing but throwaway TXT records ever
lives in it).

### 1. Cluster add-ons

```shell
just check      # what is already installed -- read before going further
just install    # Envoy Gateway + cert-manager + GatewayClass
```

`just install` enables `config.gatewayAPI.enabled=true` on cert-manager,
which is off by default and silently does nothing when forgotten, then
restarts cert-manager (it reads the Gateway API CRDs only at startup) and
prints the check.

### 2. acme-dns and the delegation

```shell
just deploy-acme-dns
just acme-dns-ip        # wait until this prints an address
just acme-dns-set-ip    # writes it into the ConfigMap and restarts the Pod
```

Then create the delegation at your registrar, in the zone of `example.com`:

| Name | Type | Value |
| --- | --- | --- |
| `auth` | `A` | the IP printed above |
| `auth` | `NS` | `auth.example.com.` |

Verify before going further — from a public resolver, not only directly:

```shell
dig +short NS auth.example.com
dig @1.1.1.1 SOA auth.example.com +short
```

### 3. The wildcard acme-dns account

A wildcard is validated against the **base** domain: the challenged name of
`*.example.com` is `example.com`, so that is the key to register.

```shell
just acme-dns-register example.com
```

It prints the `CNAME` to create at the registrar:

| Name | Type | Value |
| --- | --- | --- |
| `_acme-challenge` | `CNAME` | `<uuid>.auth.example.com.` |

Static, created once, survives every renewal.

```shell
dig +short CNAME _acme-challenge.example.com
```

Once every account you need exists, close registration: set
`disable_registration = true` in `acme-dns/configmap.yml` and re-apply.

### 4. The Gateway and the certificate

```shell
just deploy             # issuers + Gateway + redirect route, then watches
just gateway-ip
```

Create the application `A` record — a wildcard one covers every future app:

| Name | Type | Value |
| --- | --- | --- |
| `*` | `A` | the Gateway IP |

```shell
just certificate-watch  # READY=True after a minute or two
just certificate-show   # issuer must read (STAGING) at this point
```

### 5. Switch to production

Only once staging works end to end:

```shell
just use-production
just certificate-show
```

## Onboarding an application

Two steps, and no change to this directory.

**1. The `A` record**, unless the zone already has a wildcard one:
`invoices.example.com` → `just gateway-ip`.

**2. The namespace grant:**

```shell
just grant invoices        # labels it gateway-access=true
just tenants               # namespaces currently allowed
```

The application then deploys its own HTTPRoute with
`parentRefs: [{name: gateway-infra, namespace: gateway-infra, sectionName: https}]`
— which is what [`../prod_app`](../prod_app/) generates when
`gateway_listener` is left at its default, `https`. Everything else (the
redirect, the certificate, the listener) is already here.

## Adding a domain outside the wildcard

For a hostname the wildcard does not cover — a client's domain, an apex, a
second zone.

**Default path, same issuer.** Register one more acme-dns account keyed by
that exact hostname, create one static CNAME in that zone, add two listeners:

```shell
just acme-dns-register app.client-domain.com
# paste optional/extra-domain-listeners.snippet.yml into gateway/gateway.yml
kubectl apply -f gateway/gateway.yml -f optional/extra-domain-redirect-route.yml
```

Nothing else changes: the Gateway annotation keeps working and cert-manager
writes that listener's certificate like any other.

**Covering the apex too.** `*.example.com` does not cover `example.com`
itself, and the annotation cannot express a two-name certificate. Write it by
hand: see `optional/certificate-apex.yml`, which also explains why the
annotation has to be removed from the Gateway first.

**If DNS-01 is impossible for a zone** — you cannot get even one static CNAME
created in it — that hostname needs HTTP-01, i.e. a different issuer. Since
the `cert-manager.io/cluster-issuer` annotation is set on the Gateway and
applies to every HTTPS listener at once, mixing challenge types on one
Gateway means hand-writing every Certificate. Unless that is a single
exception, [`../prod_common_HTTP-01`](../prod_common_HTTP-01/) is the simpler
answer.

## Day to day

```shell
just status              # gateway, routes, certificates, acme-dns, all tenants
just describe            # per-listener conditions -- read this when PROGRAMMED=False
just certificate         # certificate, request, order, challenge
just logs-cert-manager
just logs-acme-dns
```

| Symptom | Look at |
| --- | --- |
| `PROGRAMMED=False` | `just describe` — one unresolved listener is enough |
| Certificate stuck `READY=False` | `just certificate`, then `kubectl describe challenge -n gateway-infra`; its message is the verbatim CA answer |
| `account credentials not found for domain X` | the key in `acmedns.json` must equal `X` exactly — for a wildcard, the base domain without `*.` |
| Challenge times out, `dig` shows no TXT | the `_acme-challenge` CNAME, or UDP/53 blocked to acme-dns |
| An app's route is `Accepted=False` | its namespace lacks `gateway-access=true` (`just grant <ns>`), or a wrong `sectionName` |
| `404` from Envoy for a hostname | no `A` record, or no HTTPRoute matches that hostname |

## Operating notes

- **Back up the acme-dns PVC.** The SQLite database is the only copy of every
  registration; losing it means re-registering and editing every CNAME.
- **Rate limits.** The wildcard counts as *one* name against Let's Encrypt's
  limits and replaces many. The duplicate-certificate limit (5/week, same set
  of names) is the one that hurts — do not delete `wildcard-tls` casually.
- **Renewal** is automatic at ~day 60 of 90, with no DNS change: the
  delegation and the CNAMEs are static.
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
kubectl delete -f acme-dns/
kubectl delete -f gateway-class.yml
helm uninstall cert-manager -n cert-manager
helm uninstall eg -n envoy-gateway-system
```

`helm uninstall` leaves cert-manager's CRDs in place on purpose: deleting a
CRD garbage-collects every object of that kind cluster-wide. Remove the `A`,
`NS` and `_acme-challenge` records from the zone too.
