# HTTPS with Let's Encrypt certificates (cert-manager + Gateway API)

This example builds on [`4.3.1_gateway_api_envoy_gateway`](../4.3.1_gateway_api_envoy_gateway/),
which served the app over plain HTTP. The same app is served over **HTTPS**
here, with a **publicly trusted certificate from [Let's Encrypt](https://letsencrypt.org/)**
that [cert-manager](https://cert-manager.io/) obtains, installs and renews on
its own — no `openssl`, no file to keep, no expiry date to remember.

[`5.1_tls`](../5.1_tls/) did the same HTTPS plumbing with a **self-signed**
certificate created by hand. The Gateway configuration is nearly identical;
what changes is who fills the Secret. Reading 5.1 first is recommended but not
required: everything needed is repeated below.

Once the site is served over HTTPS,
[`5.3.1_basic_auth_in_envoy`](../5.3.1_basic_auth_in_envoy/) and
[`5.3.2_basic_auth_in_nginx`](../5.3.2_basic_auth_in_nginx/) put a password in
front of it — which only becomes safe to do once this example is in place.
Both *continue* this one rather than repeating it, on the same namespace and
the same domain, so if you intend to go there next, run this example to the
end and stop before *Remove the demo*.

## What changes compared to `4.3.1_gateway_api_envoy_gateway`

The app itself does not change at all. `deployment.yml` and `service.yml` are
copied verbatim from 4.3.1, and the nginx Pod still speaks plain HTTP on
port 80, unaware that anything is encrypted.

| | `4.3.1` | `5.2` (here) |
| --- | --- | --- |
| Listeners on the Gateway | one, `HTTP:80` | two, `HTTP:80` and `HTTPS:443` |
| Listener `hostname` | none (any host) | `my-app.example.com`, required |
| Certificate | none | issued by Let's Encrypt into a Secret |
| HTTPRoutes | one | two: the app on `https`, a 301 redirect on `http` |
| Extra manifest | — | `cluster-issuer.yml` |
| Cluster add-on | Envoy Gateway | Envoy Gateway **+ cert-manager** |
| Needs a public IP | no | **yes** |
| Needs a real domain name | no | **yes** |

Concretely, four things are new:

1. **cert-manager** is installed on the cluster, with its Gateway API
   integration enabled;
2. a **ClusterIssuer** (`cluster-issuer.yml`) describes the Let's Encrypt
   account and how domain ownership is proven;
3. `gateway.yml` gains an **HTTPS listener** and one **annotation**,
   `cert-manager.io/cluster-issuer`, which is the entire trigger;
4. the routes gain hostnames, split across the two listeners, and a redirect
   route sends plain HTTP to HTTPS.

The last two rows of the table are the real cost of this example:
Let's Encrypt validates the domain by connecting to it **from the internet**,
so a local cluster (minikube, kind, a k3s on your laptop) cannot work here.
5.1 has no such constraint.

## TLS termination, unchanged

As in 5.1, the certificate belongs to the **Gateway**, not to the
application. The Envoy proxy provisioned by the controller decrypts the
incoming traffic and forwards plain HTTP to the Service:

```
internet --HTTPS--> Gateway (Envoy, holds the certificate) --HTTP--> Service --> Pods
```

Certificates live in one place, owned by whoever operates the Gateway, and
applications stay unaware of them.

## How cert-manager works

cert-manager is a Kubernetes **operator**: a controller plus a set of CRDs.
You describe the certificate you want, it makes the cluster match that
description and keeps it matching — which is what makes renewal a non-event.

### The objects

- **Issuer** / **ClusterIssuer** — *where certificates come from*: an ACME
  account at Let's Encrypt, a private CA, a Vault instance, or `selfSigned`.
  `Issuer` is namespaced; `ClusterIssuer` is cluster-scoped and usable from
  every namespace. This example uses ClusterIssuers.
- **Certificate** — *what you want*: hostnames, the issuer to ask, and the
  name of the Secret to write. This is the object you would normally write by
  hand; here it is generated (see below).
- **Secret** — *the result*: an ordinary `kubernetes.io/tls` Secret holding
  `tls.crt` and `tls.key`, exactly the kind created by hand in 5.1. This is
  the only object the Gateway ever reads; cert-manager could be uninstalled
  and HTTPS would keep working until expiry.

Three more objects appear during issuance, and exist mostly so that failures
have somewhere to be reported: **CertificateRequest** (one attempt at getting
one certificate signed), and, for ACME issuers, **Order** and **Challenge**
(one per hostname to validate). Following that chain is how you debug, so it
is worth knowing the order:

```
Certificate -> CertificateRequest -> Order -> Challenge -> ... -> Secret
```

### The trigger: an annotation on the Gateway

No `Certificate` object appears in this directory. Instead, a cert-manager
component known as the **gateway-shim** watches Gateways carrying the
`cert-manager.io/cluster-issuer` (or `cert-manager.io/issuer`) annotation, and
writes the Certificate for you, one per eligible HTTPS listener. It is the
Gateway API counterpart of the `cert-manager.io/cluster-issuer` annotation on
an Ingress.

A listener is eligible only if all of the following hold — a listener that
fails any of them is skipped silently, which is the most common reason for
"nothing happens":

| Field | Requirement |
| --- | --- |
| `hostname` | must not be empty (it becomes the certificate's `dnsNames`) |
| `tls.mode` | must be `Terminate` (`Passthrough` is not supported) |
| `tls.certificateRefs[].name` | must be set (it becomes the Secret *and* the Certificate name) |
| `tls.certificateRefs[].namespace` | if set, must be the Gateway's own namespace |

Writing the `Certificate` yourself is equally valid, and preferable as soon as
you want options the annotation cannot express (extra SANs, a specific key
algorithm, a non-default duration). The annotation just keeps the common case
to one line.

### Proving the domain is yours: the ACME HTTP-01 challenge

Let's Encrypt signs a certificate for `my-app.example.com` only once it has
checked that you control that name. That protocol is **ACME**, and this
example uses its **HTTP-01** challenge, which works like this:

1. cert-manager asks Let's Encrypt for a certificate (an ACME *order*);
2. Let's Encrypt answers with a random token;
3. cert-manager creates a **temporary Pod, Service and HTTPRoute** serving
   that token at `http://my-app.example.com/.well-known/acme-challenge/<token>`;
4. Let's Encrypt resolves the domain in public DNS and fetches that URL **over
   plain HTTP, from the internet**;
5. on success, it signs the certificate; cert-manager stores it in the Secret
   and deletes the three temporary objects.

Step 4 is where the prerequisites come from: the DNS record must be public and
correct, and port 80 must be reachable from outside. It is also why the
`http` listener has to stay on the Gateway — the challenge is *never* served
over HTTPS, since the whole point is that there is no certificate yet.

The temporary HTTPRoute is attached to the Gateway named in the issuer's
`solvers[].http01.gatewayHTTPRoute.parentRefs`, which is why `cluster-issuer.yml`
mentions this demo's Gateway by name and namespace. cert-manager never edits
the Gateway itself.

The alternative, **DNS-01**, proves ownership by writing a TXT record through
your DNS provider's API. It needs no public IP and no open port 80, and it is
the only way to get **wildcard** certificates — at the price of credentials
for your DNS zone. If this demo cannot reach your cluster from the internet,
DNS-01 is the way out, and
[`5.5_lets_encrypt_DNS-01`](../5.5_lets_encrypt_DNS-01/) is this same example
done that way, without handing anyone the keys to your zone.

### Renewal

A Let's Encrypt certificate is valid for **90 days**. cert-manager renews at
two thirds of its lifetime, i.e. roughly **30 days before expiry**, by running
the same flow again and overwriting the Secret. Envoy Gateway watches the
Secret and reloads the proxy — no restart, no downtime, nothing to do. That
automation is the entire reason cert-manager exists, and the one thing 5.1
could not offer.

## Prerequisites

- **Envoy Gateway and the `eg` GatewayClass**, installed exactly as in
  [`4.3.1_gateway_api_envoy_gateway`](../4.3.1_gateway_api_envoy_gateway/README.md#prerequisite-a-gateway-api-implementation)
  — including the checks to make before installing anything cluster-wide. In
  short, if `kubectl get gatewayclass` already lists a class whose
  `CONTROLLER` is `gateway.envoyproxy.io/gatewayclass-controller`, reuse it
  (set its name in `spec.gatewayClassName` of `gateway.yml`), otherwise:

  ```shell
  helm install eg oci://docker.io/envoyproxy/gateway-helm --version v1.9.1 -n envoy-gateway-system --create-namespace
  kubectl wait --timeout=5m -n envoy-gateway-system deployment/envoy-gateway --for=condition=Available
  kubectl apply -f gateway-class.yml
  ```

- **A cluster whose Gateway gets a public IP**, reachable from the internet on
  ports 80 and 443. In practice: a cloud cluster. Check that your provider's
  firewall or security groups let port 80 through — it is often the forgotten
  one, and HTTP-01 needs exactly that.

- **A domain name you own**, with a DNS `A` record pointing at the Gateway
  address. Chicken and egg: the address only exists once the Gateway is
  applied, so the order is *apply the Gateway → read its address → create the
  DNS record → let cert-manager work*. The walkthrough below follows that
  order.

- **cert-manager**, installed next.

Replace `my-app.example.com` with your own domain everywhere
(`gateway.yml`, `http-route.yml`, `http-redirect-route.yml`) and
`you@example.com` with your address in `cluster-issuer.yml`:

```shell
sed -i 's/my-app\.example\.com/www.your-domain.com/g' gateway.yml http-route.yml http-redirect-route.yml
sed -i 's/you@example\.com/your-address@your-domain.com/g' cluster-issuer.yml
```

## Installing cert-manager

### Is it already installed?

cert-manager is a cluster-wide add-on shared by every application on the
cluster, so check before installing anything. An empty output or a `NotFound`
error means it is absent:

```shell
kubectl get deployments -n cert-manager
kubectl api-resources --api-group=cert-manager.io
helm list --all-namespaces
```

If it is already there, skip the `helm install` and jump to *Check the Gateway
API integration* below — the integration still has to be enabled, and it is
off by default.

### Installing it

Install the chart, its CRDs, and the Gateway API integration in one go:

```shell
helm install cert-manager oci://quay.io/jetstack/charts/cert-manager \
  --version v1.21.2 \
  --namespace cert-manager --create-namespace \
  --set crds.enabled=true \
  --set config.gatewayAPI.enabled=true
```

- `crds.enabled=true` installs the `Certificate`, `Issuer`, `ClusterIssuer`,
  `Order`, `Challenge`... CRDs along with the controller. It is off by default
  because CRDs are cluster-wide and shared; installing them from the chart is
  the simplest option when nothing else on the cluster owns them.
- `config.gatewayAPI.enabled=true` is what makes cert-manager look at Gateway
  objects at all. **Without it, the annotation in `gateway.yml` is ignored and
  nothing happens** — no Certificate, no error, no event. (This nested
  spelling was introduced in cert-manager 1.21; older releases, and most
  tutorials you will find, use `config.enableGatewayAPI=true`, still accepted
  but deprecated. Before 1.15 the `ExperimentalGatewayAPISupport` feature gate
  was needed on top.)

The chart deploys three Deployments — `cert-manager` (the controller),
`cert-manager-webhook` (validates and defaults the CRDs) and
`cert-manager-cainjector` (feeds CA bundles to that webhook). Wait for them:

```shell
kubectl wait --timeout=5m -n cert-manager deployment --all --for=condition=Available
kubectl get pods -n cert-manager
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

If you prefer to read it from the running process, the flag ends up in the
controller's own configuration; the controller log at startup is the other
place to look:

```shell
kubectl logs -n cert-manager deployment/cert-manager | head -20
```

See the [cert-manager installation documentation](https://cert-manager.io/docs/installation/helm/)
for the other options (`kubectl apply` of a static manifest, operators, ...).

## Create the issuers

```shell
kubectl create namespace snippet-letsencrypt-demo
kubectl apply -f cluster-issuer.yml
```

`cluster-issuer.yml` declares two ClusterIssuers, `letsencrypt-staging` and
`letsencrypt`, differing only by the ACME server URL. **Always start with
staging.** Its certificates are signed by an untrusted root (so browsers still
warn), but its rate limits are loose, whereas production enforces
[limits](https://letsencrypt.org/docs/rate-limits/) that are easy to burn
through while a DNS record or a firewall rule is still wrong:

- 5 certificates per week for the same exact set of hostnames — the one that
  hurts, and the one that cannot be raised;
- 5 authorization failures per hostname per hour;
- 50 certificates per registered domain per week.

The issuers have no work to do yet, so they are ready immediately. `READY`
should be `True`; if it is not, the `REASON`/message usually points at a
malformed ACME server URL or a network problem reaching Let's Encrypt:

```shell
kubectl get clusterissuer
kubectl describe clusterissuer letsencrypt-staging
```

Registration with Let's Encrypt happens here: cert-manager creates an ACME
account keyed by the private key it just stored in
`letsencrypt-staging-account-key`, in its own namespace (a ClusterIssuer has
no namespace of its own):

```shell
kubectl get secret -n cert-manager letsencrypt-staging-account-key
```

> **On ClusterIssuer vs Issuer.** A ClusterIssuer is the common choice, and
> the one most documentation shows. Note that these two are slightly unusual:
> because the HTTP-01 solver names one specific Gateway, they are cluster-wide
> objects tied to a single namespace's Gateway. On a real cluster, a
> ClusterIssuer normally points at the shared Gateway that fronts everything,
> so that every namespace can use it. A namespaced `Issuer` (referenced with
> the `cert-manager.io/issuer` annotation) would keep this demo entirely
> self-contained instead, and would be deleted along with its namespace.

## Deploy the demo

```shell
kubectl apply \
  -f deployment.yml \
  -f service.yml \
  -f gateway.yml \
  -f http-route.yml \
  -f http-redirect-route.yml \
  -n snippet-letsencrypt-demo
```

Wait for the Gateway's `ADDRESS` column to be populated (`Ctrl+C` to stop
watching):

```shell
kubectl get gateway -n snippet-letsencrypt-demo --watch
```

`PROGRAMMED` will read `False` at this stage, and that is expected: the HTTPS
listener points at a Secret that does not exist yet. `kubectl describe` spells
it out, per listener — `ResolvedRefs: False`, *"Secret ... does not exist"* on
`https`, while `http` is fine and already serving:

```shell
kubectl describe gateway my-gateway -n snippet-letsencrypt-demo
```

That half-working state is the whole point. The `http` listener is what
carries the ACME challenge, and it is up before any certificate exists.

### Point DNS at the Gateway

Take the address:

```shell
GATEWAY_IP=$(kubectl get gateway my-gateway -n snippet-letsencrypt-demo -o jsonpath='{.status.addresses[0].value}')
echo $GATEWAY_IP
```

Create an `A` record for your domain pointing at it (or a `CNAME` if your
provider hands out a hostname rather than an IP), then wait for it to
propagate. Do not skip this check — a stale record is the single most common
cause of a failing challenge, and `curl --resolve` or `/etc/hosts` tricks,
which were fine in 5.1, are useless here: Let's Encrypt resolves the name
itself, from its own servers:

```shell
dig +short my-app.example.com
curl -i http://my-app.example.com/
```

The `curl` should answer `301` towards `https://`, proving the `http`
listener is reachable from the outside on port 80.

## Watch the certificate being issued

cert-manager reacts to the annotation as soon as the Gateway exists, and the
Certificate goes `READY=True` a minute or two after DNS resolves correctly:

```shell
kubectl get certificate -n snippet-letsencrypt-demo --watch
```

This is the object nobody wrote: it was generated by the gateway-shim from the
listener, and is named after the Secret. Its `dnsNames` come from the listener
`hostname`, its `issuerRef` from the annotation:

```shell
kubectl get certificate my-tls -n snippet-letsencrypt-demo -o yaml
```

Watch the whole chain while it works. The intermediate objects appear and
disappear within a couple of minutes:

```shell
kubectl get certificate,certificaterequest,order,challenge -n snippet-letsencrypt-demo
```

And the temporary solver objects, which exist only during the challenge — a
Pod, a Service, and an HTTPRoute named `cm-acme-http-solver-xxxxx`:

```shell
kubectl get pods,svc,httproute -n snippet-letsencrypt-demo
```

`kubectl describe challenge` is the single most useful command when this
hangs: its status message is the verbatim answer Let's Encrypt got when it
fetched the token:

```shell
kubectl describe challenge -n snippet-letsencrypt-demo
```

Once `READY` is `True`, the Secret exists — an ordinary `kubernetes.io/tls`
Secret, indistinguishable from the hand-made one in 5.1:

```shell
kubectl get secret my-tls -n snippet-letsencrypt-demo
kubectl describe secret my-tls -n snippet-letsencrypt-demo
```

Read the certificate back out of the cluster. Note the issuer: `(STAGING)`
something, from Let's Encrypt's test hierarchy, and a validity of 90 days:

```shell
kubectl get secret my-tls -n snippet-letsencrypt-demo \
  -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -subject -issuer -dates
```

The Gateway should now be fully programmed, with the HTTPS listener resolved:

```shell
kubectl get gateway -n snippet-letsencrypt-demo
```

## Test it, with the staging certificate

```shell
curl https://my-app.example.com/
```

```
curl: (60) SSL certificate problem: unable to get local issuer certificate
```

Expected, and *not* the same failure as in 5.1: the certificate is signed by a
real CA hierarchy here, it is simply Let's Encrypt's **staging** one, which no
client trusts. `-k` shows the nginx welcome page, and confirms everything but
the trust chain works:

```shell
curl -k https://my-app.example.com/
```

Look at what the Gateway serves — the issuer name is the interesting line:

```shell
openssl s_client -connect my-app.example.com:443 -servername my-app.example.com </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates
```

Check the redirect on port 80, which now that the challenge is over catches
everything:

```shell
curl -I http://my-app.example.com/
```

## Switch to the production issuer

Only once the above works end to end. Point the annotation at the real
Let's Encrypt:

```shell
sed -i 's|cert-manager.io/cluster-issuer: letsencrypt-staging|cert-manager.io/cluster-issuer: letsencrypt|' gateway.yml
kubectl apply -f gateway.yml -n snippet-letsencrypt-demo
```

cert-manager notices the `issuerRef` of the Certificate no longer matches and
re-issues it, through the same challenge:

```shell
kubectl get certificate,order,challenge -n snippet-letsencrypt-demo
```

```shell
kubectl get certificate -n snippet-letsencrypt-demo --watch
```

The issuer is now one of Let's Encrypt's production intermediates:

```shell
kubectl get secret my-tls -n snippet-letsencrypt-demo \
  -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -subject -issuer -dates
```

And plain `curl`, with no flag at all, finally works — the trust chain is the
one your system already knows:

```shell
curl https://my-app.example.com/
```

Open `https://my-app.example.com/` in a browser: a real padlock, no warning,
no `/etc/hosts` entry, nothing to add to any trust store. That is what the
whole chapter buys compared to 5.1.

## Nothing left to do

The certificate expires in 90 days and cert-manager will replace it around day
60, on its own, in place. You can see the planned dates on the Certificate:

```shell
kubectl get certificate my-tls -n snippet-letsencrypt-demo \
  -o jsonpath='{.status.notBefore} -> {.status.notAfter} (renew at {.status.renewalTime}){"\n"}'
```

To rehearse a renewal instead of waiting two months, force one — this deletes
nothing and goes through the full flow again (mind the staging/production rate
limits if you do it repeatedly):

```shell
cmctl renew my-tls -n snippet-letsencrypt-demo
```

`cmctl` is cert-manager's [command line tool](https://cert-manager.io/docs/reference/cmctl/),
installed separately (it also works as `kubectl cert-manager renew ...` when
put on the `PATH` as a kubectl plugin). Without it, the same effect is
obtained by deleting the Secret, which cert-manager immediately re-creates:

```shell
kubectl delete secret my-tls -n snippet-letsencrypt-demo
kubectl get certificate -n snippet-letsencrypt-demo --watch
```

## When it does not work

Work down the chain, in this order — each object's `status` names the next one
to look at:

```shell
kubectl describe gateway my-gateway -n snippet-letsencrypt-demo
kubectl describe certificate my-tls -n snippet-letsencrypt-demo
kubectl describe certificaterequest -n snippet-letsencrypt-demo
kubectl describe order -n snippet-letsencrypt-demo
kubectl describe challenge -n snippet-letsencrypt-demo
kubectl logs -n cert-manager deployment/cert-manager --tail=100
```

The usual suspects, in decreasing order of frequency:

- **No Certificate object is ever created.** The Gateway API integration is
  off (`config.gatewayAPI.enabled`), or cert-manager started before the
  Gateway API CRDs existed — restart it. Otherwise the listener is not
  eligible: check `hostname`, `mode: Terminate` and `certificateRefs[].name`
  against the table above.
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

## Remove the demo

Skip this section for now if you are going on to
[`5.3.1_basic_auth_in_envoy`](../5.3.1_basic_auth_in_envoy/) or
[`5.3.2_basic_auth_in_nginx`](../5.3.2_basic_auth_in_nginx/): both add a
password to the demo deployed here, and need it running.

```shell
kubectl delete \
  -f http-redirect-route.yml \
  -f http-route.yml \
  -f gateway.yml \
  -f service.yml \
  -f deployment.yml \
  -n snippet-letsencrypt-demo

kubectl delete namespace snippet-letsencrypt-demo
```

Deleting the namespace removes the Certificate and the `my-tls` Secret with
it. Remove the DNS record you created too.

The ClusterIssuers are cluster-scoped, so they survive the namespace and have
to be deleted explicitly. They are only useful to this demo — their solver
names its Gateway — but check that nobody else adopted them first:

```shell
kubectl get certificate --all-namespaces \
  -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,ISSUER:.spec.issuerRef.name'
kubectl delete -f cluster-issuer.yml
```

The ACME account keys stay behind, in cert-manager's namespace. Keeping them
is harmless and saves re-registering; delete them only if you are removing
cert-manager altogether:

```shell
kubectl delete secret letsencrypt-staging-account-key letsencrypt-account-key -n cert-manager
```

### Shared cluster add-ons: stop and check first

cert-manager, the Envoy Gateway controller and the GatewayClass are
cluster-wide and shared. **Do not delete them if you did not install them, or
if anything else on the cluster still uses them.** Check, as described in
[`4.3.1_gateway_api_envoy_gateway`](../4.3.1_gateway_api_envoy_gateway/README.md#shared-resources-stop-and-check-first):

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

`helm uninstall` leaves the cert-manager CRDs in place on purpose (the chart
sets `helm.sh/resource-policy: keep`), because deleting a CRD garbage-collects
every object of that kind — every Certificate, Issuer and ClusterIssuer on the
cluster. The `kubernetes.io/tls` Secrets survive, so HTTPS keeps working until
expiry, but nothing renews it any more. Remove the CRDs by hand, knowingly,
only if nothing else uses cert-manager:

```shell
kubectl get crd -o name | grep cert-manager.io
```
