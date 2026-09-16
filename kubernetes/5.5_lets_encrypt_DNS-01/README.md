# HTTPS with DNS-01 challenges, on any registrar (cert-manager + acme-dns)

This example serves the same application as
[`5.2_lets_encrypt`](../5.2_lets_encrypt/), over HTTPS, with the same publicly
trusted Let's Encrypt certificate obtained and renewed by
[cert-manager](https://cert-manager.io/), behind the same Gateway. One single
thing changes: **how the domain is proven to be yours**.

5.2 used the **HTTP-01** challenge — Let's Encrypt connects to your site on
port 80 and reads a token there. That is the simplest possible proof, and it
costs nothing, but it buys its simplicity with two hard requirements: the
name must resolve to *your* cluster, and port 80 must be open to the whole
internet. It also cannot produce wildcard certificates, ever.

This example uses the other challenge, **DNS-01**: instead of serving a file,
you publish a TXT record. Nothing about your cluster needs to be reachable
from the internet any more — but something now has to write into your DNS
zone, on cert-manager's behalf, every time a certificate is issued or renewed.
That is the whole difficulty of DNS-01, and the reason this example exists:
the obvious way to do it, handing cert-manager an API token for your domain,
is both the least secure and the least portable option. **acme-dns** is the
way around it, and it works the same whoever your registrar is — Gandi, OVH,
Namecheap, Infomaniak, a registrar with no API at all.

Read 5.2 first. Everything it explains — cert-manager's objects, the
gateway-shim, the annotation, the staging/production split, renewal — is
unchanged here and is not repeated.

## What changes compared to `5.2_lets_encrypt`

| | `5.2` (HTTP-01) | `5.5` (here, DNS-01) |
| --- | --- | --- |
| Proof of ownership | a token served on `http://…/.well-known/acme-challenge/…` | a TXT record at `_acme-challenge.…` |
| Who answers the CA | the Gateway, through a temporary solver Pod | a DNS server, over UDP/TCP 53 |
| Needs port 80 open on the app | **yes** | no |
| Needs the app to have a public IP | **yes** | no (only to *serve* it afterwards) |
| Needs credentials | none | **yes**, to write the TXT record |
| Wildcard certificates | impossible | **possible** |
| Temporary objects during issuance | Pod + Service + HTTPRoute | none |
| Extra component to run | — | acme-dns (one Deployment) |
| One-off manual steps | 1 DNS record | 1 delegation (`A` + `NS`), 1 registration, 1 `CNAME` |
| `http` listener on the Gateway | mandatory | optional |
| Application manifests | — | **identical** |

`deployment.yml`, `service.yml`, `http-route.yml`, `http-redirect-route.yml`
and `gateway.yml` are 5.2's files with a hardcoded namespace. The certificate
is requested by the same one-line annotation. **Only `cluster-issuer.yml`
genuinely differs** — plus the new `acme-dns/` directory, which is
infrastructure, not part of the application.

## Why DNS-01 at all

Three situations where HTTP-01 simply cannot be used, and DNS-01 is the only
answer:

- **Wildcard certificates.** Let's Encrypt issues `*.example.com` through
  DNS-01 and nothing else. Around five to ten subdomains, one wildcard starts
  being much less work than one certificate per name (see the comparison table
  in [`5.4_lets_encrypt_multi_apps`](../5.4_lets_encrypt_multi_apps/README.md#one-certificate-per-hostname)).
- **Clusters that are not publicly reachable.** An internal application, a
  cluster behind a VPN, a private load balancer, an environment where security
  policy forbids opening port 80 — all of them can still get publicly trusted
  certificates, because the CA never talks to the cluster.
- **Certificates issued before the service exists.** The DNS record does not
  have to point at anything yet.

And one situation where it is a nuisance: DNS-01 is *slower and less
deterministic*. It depends on record propagation and on caches you do not
control, so a challenge takes minutes rather than seconds, and a stale cache
is a failure mode HTTP-01 does not have.

## The problem DNS-01 creates, and the CNAME that solves it

To write the TXT record, cert-manager needs credentials for your DNS zone.
Done the obvious way, that means an API token from your registrar, and it has
three problems:

1. **Blast radius.** Registrar tokens are almost never scoped to one record.
   A token that can write `_acme-challenge.my-app.example.com` can usually
   also rewrite your `MX` records, or point `www` somewhere else. It lives in
   a Kubernetes Secret, readable by anyone with the right RBAC.
2. **Portability.** cert-manager natively supports eight providers only:
   ACMEDNS, Akamai, AzureDNS, Cloudflare, Google CloudDNS, Route53,
   DigitalOcean and RFC2136. Everything else — Gandi, OVH, Namecheap,
   Infomaniak, Hetzner… — needs a third-party *webhook*, a cluster-wide
   component whose quality and maintenance vary a lot from one provider to the
   next.
3. **Lock-in.** Change registrar and the whole mechanism changes with it.

The way out is a standard DNS feature: **delegation**. The CA does not care
*where* the TXT record lives, only that the DNS says it is authoritative for
that name. So you create, once and for all, a static `CNAME`:

```
_acme-challenge.my-app.example.com.  CNAME  <uuid>.auth.example.com.
```

From then on, whoever controls `auth.example.com` can answer the challenges
for `my-app.example.com` — and your registrar zone is never touched again.
This is `cnameStrategy: Follow` territory, and it is exactly what
cert-manager's documentation calls a *delegated domain*.

**acme-dns** is a DNS server written for that one job. It serves the
`auth.example.com` zone, it stores nothing but TXT records, and its API can do
exactly one thing: set the TXT record of the one random subdomain an account
owns.

```
  (1) cert-manager  ──POST /update──>  acme-dns      (inside the cluster,
                                           │          over plain HTTP)
                                           │ publishes
                                           v
                        TXT  <uuid>.auth.example.com  =  <token>

  (2) Let's Encrypt asks for  TXT _acme-challenge.my-app.example.com
                                           │
      your registrar's zone answers        │  CNAME — static, created once,
      with nothing but a redirection       │          grants nothing else
                                           v
                        TXT  <uuid>.auth.example.com  =  <token>   ✓
```

Compare what a leaked credential gets an attacker:

| | Registrar API token | acme-dns account |
| --- | --- | --- |
| Can rewrite `MX`, `A`, `NS` of your zone | yes, usually | no |
| Can write records for other domains of the account | yes, usually | no |
| Can serve an ACME challenge for your domain | yes | yes — that one is unavoidable |
| Revocation | rotate the token, everywhere it is used | delete one registration |

The third line is worth stating plainly: an acme-dns account *is* enough to
obtain a certificate for the names whose `_acme-challenge` CNAME points at it.
Delegation reduces the damage, it does not eliminate it — which is precisely
why the upstream project insists you run your **own** acme-dns instance rather
than the public one it operates for testing.

## acme-dns in three endpoints

The whole server is one Go binary with a REST API of three routes:

| Endpoint | Called by | What it does |
| --- | --- | --- |
| `POST /register` | you, **once**, by hand | invents a random subdomain (`<uuid>.auth.example.com`) and returns it with a username and a password |
| `POST /update` | cert-manager, at every issuance and renewal | sets the TXT value of *that* subdomain, authenticated by `X-Api-User` / `X-Api-Key` |
| `GET /health` | Kubernetes probes | liveness/readiness |

Two details matter later:

- acme-dns keeps the **two most recent TXT values** of a subdomain, rolling.
  That is not an implementation accident: a certificate covering both
  `example.com` and `*.example.com` produces two simultaneous challenges at
  the *same* `_acme-challenge.example.com` name, and both answers have to be
  published at once. This is where several registrar webhooks fall over.
- cert-manager's acmeDNS solver implements `/update` only. It **never
  registers** an account and **never cleans up** a record: the last TXT value
  stays published after issuance. It is harmless — it lives in a zone that
  contains nothing else — and it is by design.

## Layout

```
gateway-class.yml            # cluster-wide, as in 4.3.1 / 5.2

acme-dns/                    # namespace snippet-acme-dns — the new component
├── namespace.yml
├── configmap.yml            # config.cfg: the zone name and the public IP
├── pvc.yml                  # the registrations database (the only copy!)
├── deployment.yml           # the server itself
├── service-dns.yml          # LoadBalancer, UDP+TCP 53 — the only public part
└── service-api.yml          # ClusterIP — /register and /update, internal only

namespace.yml                # namespace snippet-letsencrypt-dns01-demo
cluster-issuer.yml           # THE file that differs from 5.2
gateway.yml                  # 5.2's, unchanged but for the namespace
deployment.yml               # \
service.yml                  #  |  5.2's application, verbatim
http-route.yml               #  |
http-redirect-route.yml      # /
```

The two namespaces reflect two lifetimes. `snippet-acme-dns` is
infrastructure: installed once, shared by every application, every namespace
and even every cluster you own. `snippet-letsencrypt-dns01-demo` is this demo,
deleted at the end.

## Prerequisites

- **Envoy Gateway and the `eg` GatewayClass**, as in
  [4.3.1](../4.3.1_gateway_api_envoy_gateway/README.md#prerequisite-a-gateway-api-implementation)
  — including the checks to make before installing anything cluster-wide.
- **cert-manager, with its Gateway API integration enabled**, exactly as in
  [5.2](../5.2_lets_encrypt/README.md#installing-cert-manager).
  `config.gatewayAPI.enabled=true` is the setting that is off by default and
  silently does nothing when forgotten.
- **A domain name you own**, with the ability to create `A`, `NS` and `CNAME`
  records in its zone. *Which* registrar or DNS host is irrelevant — that is
  the point of this example — and no API token is needed from them.
- **A stable public IP address for acme-dns**, reachable on **UDP and TCP port
  53**.

That last one deserves honesty, because it is easy to oversell DNS-01:

> **DNS-01 frees your application from needing a public address — it does not
> free acme-dns from needing one.** A DNS server that a certificate authority
> cannot query is useless. What you gain is that the exposed surface is one
> DNS server serving one throwaway zone, instead of your application on port
> 80; and that this one server can be shared by every private cluster you own,
> so the cost is paid once.
>
> Two practical consequences: the address must be an **IP**, because a DNS
> delegation cannot point at a `CNAME` (if your cloud hands out a hostname for
> LoadBalancers, as AWS ELBs do, you need a load balancer with static IPs
> instead); and your provider's firewall must let **UDP/53** through, which is
> the port most often forgotten. acme-dns does not have to run in this
> cluster: a €3 VPS is a perfectly good — arguably better — home for it.

Finally, replace the placeholders. `my-app.example.com` is the application,
`auth.example.com` the zone delegated to acme-dns (a subdomain of any domain
you own), `you@example.com` your contact address:

```shell
sed -i 's/my-app\.example\.com/my-app.your-domain.com/g' gateway.yml http-route.yml http-redirect-route.yml
sed -i 's/auth\.example\.com/auth.your-domain.com/g' acme-dns/configmap.yml
sed -i 's/you\.example\.com/you.your-domain.com/g' acme-dns/configmap.yml
sed -i 's/you@example\.com/you@your-domain.com/g' cluster-issuer.yml
```

## Step 1 — deploy acme-dns

```shell
kubectl apply \
  -f acme-dns/namespace.yml \
  -f acme-dns/configmap.yml \
  -f acme-dns/pvc.yml \
  -f acme-dns/deployment.yml \
  -f acme-dns/service-api.yml \
  -f acme-dns/service-dns.yml
```

```shell
kubectl get pods,svc,pvc -n snippet-acme-dns
```

The Pod should be `Running` and ready within a few seconds — the configuration
it starts with is valid, it merely advertises a placeholder IP, which is fixed
two commands from now. If the Pod stays `Pending`, the PVC has no storage
class to bind to; if it crash-loops, read the logs, as acme-dns is explicit
about a bad configuration file:

```shell
kubectl logs -n snippet-acme-dns deployment/acme-dns
```

Now wait for the load balancer address (`Ctrl+C` to stop watching), which is
the chicken-and-egg step of this example, as the Gateway address was in 5.2:

```shell
kubectl get svc acme-dns -n snippet-acme-dns --watch
```

```shell
ACME_DNS_IP=$(kubectl get svc acme-dns -n snippet-acme-dns -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo $ACME_DNS_IP
```

An empty value, with the Service stuck in `<pending>`, is almost always the
mixed-protocol load balancer: see *When it does not work*.

Put that address into the zone acme-dns serves for itself, and restart it so
it reads the file again (a ConfigMap change never restarts a Pod on its own):

```shell
sed -i "s/203\.0\.113\.1/$ACME_DNS_IP/" acme-dns/configmap.yml
kubectl apply -f acme-dns/configmap.yml
kubectl rollout restart deployment acme-dns -n snippet-acme-dns
kubectl rollout status deployment acme-dns -n snippet-acme-dns
```

## Step 2 — delegate a zone to it

In the zone of `your-domain.com`, at your registrar, create **two** records —
and note that neither of them is an API call, a token, or anything that will
ever have to change again:

| Name | Type | Value |
| --- | --- | --- |
| `auth` | `A` | the address in `$ACME_DNS_IP` |
| `auth` | `NS` | `auth.your-domain.com.` (mind the trailing dot) |

The `NS` record is the delegation: it tells the world that everything under
`auth.your-domain.com` is answered by another server. The `A` record is what
makes that possible — since the name server's own name lives *inside* the
delegated zone, resolvers would otherwise have no way to find its address.
This is the same "glue record" arrangement every registrar uses for its own
name servers.

Check the delegation before going further. Delegations propagate in seconds to
minutes, but a wrong one is the single most common reason for everything below
to fail:

```shell
# The parent zone now delegates to your server
dig +short NS auth.your-domain.com

# Your server answers for its zone — asked directly, bypassing every cache
dig @$ACME_DNS_IP SOA auth.your-domain.com +short

# ... and from a public resolver, which is what actually matters
dig @1.1.1.1 SOA auth.your-domain.com +short
```

The SOA should name `auth.your-domain.com` and the contact address you put in
`nsadmin`. If the direct query works and the public one does not, the
delegation is wrong or has not propagated; if neither works, UDP/53 is
filtered, or the Service does not reach the Pod.

## Step 3 — register an account

The API is deliberately not published on the internet, so reach it through a
port-forward. In one terminal:

```shell
kubectl port-forward -n snippet-acme-dns svc/acme-dns-api 8080:80
```

In another, register — this is the only time you will ever call this endpoint:

```shell
curl -sS -X POST http://127.0.0.1:8080/register | tee registration.json
```

```json
{
  "username": "c36f50e8-4632-44f0-83fe-e070fef28a10",
  "password": "htB9mR9DYgcu9bX_afHF62erXaH2TS7bg9KW3F7Z",
  "fulldomain": "8e5700ea-a4bf-41c7-8a77-e990661dcc6a.auth.your-domain.com",
  "subdomain": "8e5700ea-a4bf-41c7-8a77-e990661dcc6a",
  "allowfrom": []
}
```

**Keep this output.** `fulldomain` is what the CNAME of step 4 points at, and
the username/password pair is the only thing that can ever update that record.
There is no way to retrieve it later: losing it means registering again and
editing the CNAME.

cert-manager expects that object wrapped in a map **keyed by the exact domain
name being validated**:

```shell
jq '{"my-app.your-domain.com": .}' registration.json > acmedns.json
cat acmedns.json
```

Without `jq`, any editor will do — or Python:

```shell
python3 -c 'import json; r=json.load(open("registration.json")); print(json.dumps({"my-app.your-domain.com": r}, indent=2))' > acmedns.json
```

Then hand it to cert-manager, **in cert-manager's own namespace**:

```shell
kubectl create secret generic acme-dns-credentials -n cert-manager --from-file=acmedns.json
```

That namespace is not a detail. `cluster-issuer.yml` declares *ClusterIssuers*,
which are cluster-scoped and therefore have no namespace of their own; every
Secret they reference is read from cert-manager's namespace (the
`--cluster-resource-namespace` flag, `cert-manager` by default). A namespaced
`Issuer` would read it from its own namespace instead. Putting this Secret
next to the Gateway is the classic mistake, and it fails with a plain
`secret "acme-dns-credentials" not found`.

The local copies contain a password. Store them with a dedicated tool (SOPS,
Sealed Secrets, an external secret store), or delete them once the Secret
exists:

```shell
shred -u registration.json acmedns.json   # only once you are sure it works
```

## Step 4 — point the application's challenge name at that subdomain

One more record at the registrar, in the zone of `your-domain.com`, using the
`fulldomain` from step 3:

| Name | Type | Value |
| --- | --- | --- |
| `_acme-challenge.my-app` | `CNAME` | `8e5700ea-….auth.your-domain.com.` |

This is the record that makes everything work, and the last one you will touch
for this certificate: it is static, it survives every renewal, and it grants
nothing but the ability to answer ACME challenges.

```shell
dig +short CNAME _acme-challenge.my-app.your-domain.com
dig +short TXT _acme-challenge.my-app.your-domain.com
```

The `CNAME` must resolve. The `TXT` is legitimately empty for now: no
challenge has run yet, and acme-dns has nothing to answer with until one
runs.

## Step 5 — the issuers, the Gateway and the application

```shell
kubectl apply -f gateway-class.yml   # unless one already exists, see 4.3.1
kubectl apply \
  -f namespace.yml \
  -f cluster-issuer.yml \
  -f gateway.yml \
  -f deployment.yml \
  -f service.yml \
  -f http-route.yml \
  -f http-redirect-route.yml
```

The issuers should be `READY=True` immediately — they have no work to do yet,
they merely register an ACME account:

```shell
kubectl get clusterissuer
kubectl describe clusterissuer letsencrypt-staging
```

The Gateway behaves exactly as in 5.2: an address appears, `PROGRAMMED` stays
`False` while the `https` listener points at a Secret that does not exist yet.

```shell
kubectl get gateway -n snippet-letsencrypt-dns01-demo --watch
```

### One `A` record for the application — but not for the same reason

```shell
GATEWAY_IP=$(kubectl get gateway my-gateway -n snippet-letsencrypt-dns01-demo -o jsonpath='{.status.addresses[0].value}')
echo $GATEWAY_IP
```

Create an `A` record for `my-app.your-domain.com` pointing at it — **to serve
the site**, not to obtain the certificate. This is the one difference that
makes DNS-01 worth the trouble: in 5.2 this record had to exist and be correct
*before* Let's Encrypt would issue anything. Here the certificate is issued
whether this record exists or not, and on a private cluster you would put the
Gateway address in `/etc/hosts`, or in an internal DNS zone, and never publish
it at all.

## Watch the certificate being issued

```shell
kubectl get certificate -n snippet-letsencrypt-dns01-demo --watch
```

The chain is the one 5.2 described —
`Certificate → CertificateRequest → Order → Challenge → Secret` — with one
visible difference:

```shell
kubectl get certificate,certificaterequest,order,challenge -n snippet-letsencrypt-dns01-demo
kubectl get pods,svc,httproute -n snippet-letsencrypt-dns01-demo
```

**There is no solver Pod, no solver Service and no solver HTTPRoute.** Nothing
is deployed to answer the challenge, because nothing in the cluster is asked
anything: the answer is published in the DNS.

While the Challenge is in flight, its `status` says `Presented` and you can
watch the token appear in public DNS — this is the whole mechanism, visible in
one command:

```shell
kubectl describe challenge -n snippet-letsencrypt-dns01-demo
dig +short TXT _acme-challenge.my-app.your-domain.com
```

The string returned by `dig` is the value Let's Encrypt is about to check. The
acme-dns log shows the moment cert-manager wrote it:

```shell
kubectl logs -n snippet-acme-dns deployment/acme-dns --tail=20
```

A minute or two later the Certificate is `READY=True`, the Secret exists, and
the Gateway is fully programmed:

```shell
kubectl get certificate,secret -n snippet-letsencrypt-dns01-demo
kubectl get gateway -n snippet-letsencrypt-dns01-demo
kubectl get secret my-tls -n snippet-letsencrypt-dns01-demo \
  -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -subject -issuer -dates
```

The issuer line reads `(STAGING)`, from Let's Encrypt's test hierarchy, which
no client trusts. That is expected.

## Test it, with the staging certificate

```shell
curl https://my-app.your-domain.com/     # fails: unknown issuer, as in 5.2
curl -k https://my-app.your-domain.com/  # the nginx welcome page
curl -I http://my-app.your-domain.com/   # 301 to https, from the first second
```

The last one is worth a look: in 5.2 the redirect had to coexist with the
challenge route on port 80. Here port 80 carries nothing else, ever.

## Switch to the production issuer

Only once the above works end to end:

```shell
sed -i 's|cert-manager.io/cluster-issuer: letsencrypt-staging|cert-manager.io/cluster-issuer: letsencrypt|' gateway.yml
kubectl apply -f gateway.yml
kubectl get certificate,order,challenge -n snippet-letsencrypt-dns01-demo --watch
```

Nothing else changes: the same acme-dns account, the same CNAME, the same TXT
record. Then, with no flag at all:

```shell
curl https://my-app.your-domain.com/
kubectl get secret my-tls -n snippet-letsencrypt-dns01-demo \
  -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -issuer -dates
```

## The payoff: a wildcard certificate

This is what HTTP-01 can never do. A single certificate for
`*.your-domain.com` covers every subdomain, present and future, and a new application behind the
same Gateway needs no new certificate, no new challenge and no new DNS record
beyond its own `A`.

Three things change, and one trap is worth knowing about.

**1. A second acme-dns account, for the base domain.** A wildcard is validated
against the *base* name: the challenge for `*.your-domain.com` is published at
`_acme-challenge.your-domain.com`. Register a second account — with the
port-forward of step 3 still running — and key it by the base domain:

```shell
curl -sS -X POST http://127.0.0.1:8080/register > registration-wildcard.json
jq -s '{"my-app.your-domain.com": .[0], "your-domain.com": .[1]}' registration.json registration-wildcard.json > acmedns.json
kubectl delete secret acme-dns-credentials -n cert-manager
kubectl create secret generic acme-dns-credentials -n cert-manager --from-file=acmedns.json
```

> **The trap.** cert-manager looks the account up by **exact match** on the
> challenged name, and the challenged name of a wildcard has its `*.` stripped.
> The key must be `your-domain.com` — `"*.your-domain.com"` produces
> `account credentials not found for domain your-domain.com` and nothing else
> happens. One file can hold as many accounts as you have names.

**2. The CNAME for the base domain**, at the registrar:

| Name | Type | Value |
| --- | --- | --- |
| `_acme-challenge` | `CNAME` | the new `fulldomain`, e.g. `4a1f….auth.your-domain.com.` |

**3. The listener hostname**, in `gateway.yml`:

```yaml
    - name: https
      protocol: HTTPS
      port: 443
      hostname: "*.your-domain.com"
      tls:
        mode: Terminate
        certificateRefs:
          - name: my-tls
```

The gateway-shim turns that into a Certificate whose `dnsNames` is
`*.your-domain.com`, and the HTTPRoute keeps its precise hostname —
`my-app.your-domain.com` intersects the listener's wildcard, which is all the
Gateway API requires.

A wildcard does **not** cover the base domain itself: a certificate valid for
both needs `dnsNames: ["your-domain.com", "*.your-domain.com"]`, which the
annotation cannot express — write the `Certificate` by hand for that, as 5.2
describes. Both names then challenge at the *same*
`_acme-challenge.your-domain.com` record, simultaneously; acme-dns publishes
both values because it keeps the two most recent ones, which is exactly the
case it was built for.

Rate limits are the ones listed in
[5.4](../5.4_lets_encrypt_multi_apps/README.md#lets-encrypt-limits-with-several-hostnames);
a wildcard counts as one name against them, and replaces many.

## Renewal

Unchanged from 5.2, and this is where the setup pays off: cert-manager renews
around day 60 of the certificate's 90, by running the same flow again — one
`POST /update`, one TXT record, one Secret rewritten, one proxy reloaded. **No
DNS record is ever created or edited**: the delegation and the CNAMEs are
static. Nothing in your registrar account has to be touched again, by anyone.

```shell
kubectl get certificate my-tls -n snippet-letsencrypt-dns01-demo \
  -o jsonpath='{.status.notBefore} -> {.status.notAfter} (renew at {.status.renewalTime}){"\n"}'
```

To rehearse it — minding the duplicate-certificate limit of 5 per week:

```shell
cmctl renew my-tls -n snippet-letsencrypt-dns01-demo
```

## Hardening what you just deployed

The demo leaves two doors open on purpose, both cheap to close:

- **The registration endpoint.** `disable_registration = false` lets anyone who
  reaches the API create an account. That API is a ClusterIP Service, so
  "anyone" means anything running in the cluster — still worth closing once
  your accounts exist:

  ```shell
  sed -i 's/disable_registration = false/disable_registration = true/' acme-dns/configmap.yml
  kubectl apply -f acme-dns/configmap.yml
  kubectl rollout restart deployment acme-dns -n snippet-acme-dns
  ```

- **Who may update a record.** A registration can be restricted to source
  networks, which is checked on every `/update`. It can only be set **at
  registration time**, so using it means registering again and editing the
  CNAME:

  ```shell
  # What cert-manager's calls come from today — a Pod IP, which will change
  kubectl get pod -n cert-manager -l app.kubernetes.io/name=cert-manager -o wide
  curl -sS -X POST http://127.0.0.1:8080/register \
    -H 'Content-Type: application/json' \
    -d '{"allowfrom": ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]}'
  ```

  Use the Pod network range rather than one Pod's address, or the first
  restart of cert-manager breaks renewals — a failure that would surface sixty
  days later, which is the worst kind.

Two more, for a real deployment: back up the PVC (it holds credentials that
cannot be recovered), and switch the database to PostgreSQL if acme-dns ever
needs more than one replica.

## When it does not work

Work down the same chain as in 5.2, then look at the DNS:

```shell
kubectl describe certificate my-tls -n snippet-letsencrypt-dns01-demo
kubectl describe order -n snippet-letsencrypt-dns01-demo
kubectl describe challenge -n snippet-letsencrypt-dns01-demo
kubectl logs -n cert-manager deployment/cert-manager --tail=100
kubectl logs -n snippet-acme-dns deployment/acme-dns --tail=50
```

The usual suspects, in decreasing order of frequency:

- **The Challenge stays `pending`, message "self check failed".** cert-manager
  verifies the record itself before asking the CA, and this is where a broken
  delegation shows up. Reproduce it by hand:
  `dig +short TXT _acme-challenge.my-app.your-domain.com`. If `dig` shows the
  token and cert-manager does not see it, the cluster's own resolver is the
  problem — point cert-manager at public resolvers:
  `--set 'extraArgs={--dns01-recursive-nameservers=8.8.8.8:53\,1.1.1.1:53,--dns01-recursive-nameservers-only=true}'`.
  (cert-manager releases after 1.21 also accept a `nameservers` list on the
  solver itself, which avoids changing a controller-wide flag.)
- **The same, with nothing in `dig`.** The CNAME is missing or misspelled
  (a trailing dot, or a provider that silently appended the zone twice —
  `_acme-challenge.my-app.your-domain.com.your-domain.com` is a classic), or
  the `NS` delegation of `auth` is wrong. Check both:
  `dig +short CNAME _acme-challenge.my-app.your-domain.com` and
  `dig +short NS auth.your-domain.com`.
- **`account credentials not found for domain …`** in the cert-manager log.
  The key in `acmedns.json` does not match the challenged name exactly: a
  `*.` prefix, a trailing dot, the parent zone instead of the full name. The
  error message states the name cert-manager looked for; that string is what
  the key must be.
- **`secret "acme-dns-credentials" not found`.** It was created in the wrong
  namespace: a ClusterIssuer reads it from cert-manager's.
- **The acme-dns Service never gets an `EXTERNAL-IP`.** Its single Service
  carries UDP and TCP on port 53, and some cloud load balancers still refuse
  mixed protocols. Split it in two (two Services, each with one protocol,
  each with its own `spec.type: LoadBalancer`) and give the `A` record the UDP
  one, or use a provider annotation to pin both to the same address.
- **Everything resolves, and Let's Encrypt still reports `DNS problem:
  NXDOMAIN` or a timeout.** UDP/53 is filtered by the cloud firewall, or the
  address in the `A` record is not the load balancer's. Query your server from
  outside the cluster: `dig @<ip> TXT <uuid>.auth.your-domain.com`.
- **HTTP 401 in the acme-dns log.** Wrong username/password in the Secret, or
  an `allowfrom` that no longer matches cert-manager's Pod IP.
- **A stale TXT record after a successful issuance.** Expected: cert-manager's
  acme-dns solver does not clean up. It is overwritten at the next challenge.

## What this costs you

An honest summary, since the point of this example is the trade-off and not
the technology:

| | HTTP-01 (5.2) | DNS-01 + registrar token | DNS-01 + acme-dns (here) |
| --- | --- | --- | --- |
| Components to run | none | none (native) or a webhook | **one Deployment + a volume** |
| Credentials at risk | none | the whole DNS zone | one throwaway subdomain |
| Works with any registrar | yes | only 8 natively | **yes** |
| Wildcards | no | yes | yes |
| App must be publicly reachable | **yes** | no | no |
| Something must be publicly reachable | the app, on :80 | nothing | **acme-dns, on :53** |
| Manual steps per certified name | one `A` record | one API token, once | one `CNAME` |
| Who has to trust what | — | cert-manager holds your zone | acme-dns can answer challenges for the delegated names |

acme-dns is worth it when you have several domains, several clusters, or a
registrar cert-manager does not support — and it is a poor trade for a single
public application whose port 80 is open anyway, where 5.2 remains the right
answer. Between the two, delegating `_acme-challenge` to a zone hosted at a
natively supported provider (Cloudflare, Route53…) achieves the same isolation
with no component to run, at the price of an account there.

## Remove the demo

```shell
kubectl delete namespace snippet-letsencrypt-dns01-demo
```

That takes the Gateway, the application, the Certificate and the `my-tls`
Secret with it. Remove the `A` record for `my-app` too.

The ClusterIssuers are cluster-scoped and survive the namespace. Check that
nobody else adopted them first:

```shell
kubectl get certificate --all-namespaces \
  -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,ISSUER:.spec.issuerRef.name'
kubectl delete -f cluster-issuer.yml
kubectl delete secret acme-dns-credentials -n cert-manager
kubectl delete secret letsencrypt-staging-account-key letsencrypt-account-key -n cert-manager
```

If you are keeping acme-dns — and it is the one piece here worth keeping, as
it serves every future domain and cluster — stop at that point. Otherwise:

```shell
kubectl delete namespace snippet-acme-dns
```

and remove the `A`, `NS` and `_acme-challenge` `CNAME` records from your zone.
Deleting the namespace deletes the PVC, and with it every registration: any
CNAME still pointing at that server becomes a dead end, and the certificates
relying on it stop renewing — silently, sixty days later.

### Shared cluster add-ons: stop and check first

cert-manager, the Envoy Gateway controller and the GatewayClass are
cluster-wide and shared. **Do not delete them if you did not install them, or
if anything else on the cluster still uses them.** The checks, and the warning
about deleting cert-manager's CRDs, are in
[5.2](../5.2_lets_encrypt/README.md#shared-cluster-add-ons-stop-and-check-first).
