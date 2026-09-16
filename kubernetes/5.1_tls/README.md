# HTTPS with a self-signed TLS certificate (Gateway API)

This example builds on [`4.3.1_gateway_api_envoy_gateway`](../4.3.1_gateway_api_envoy_gateway/),
which served the app over plain HTTP. Here, the same app is served over
**HTTPS**, with a **self-signed certificate** created by hand with `openssl`
and handed to the Gateway through a Kubernetes **Secret**.

Nothing new is needed on the cluster: no cert-manager, no certificate
authority, no domain name that actually resolves. That makes it the shortest
path to a working HTTPS listener, and the right way to see what a certificate
*is* before letting a tool manage it for you
([`5.2_lets_encrypt`](../5.2_lets_encrypt/) does exactly that, with real
Let's Encrypt certificates).

## TLS termination

The certificate is attached to the **Gateway**, not to the application. The
Envoy proxy provisioned by the controller terminates TLS: it decrypts the
incoming traffic, then forwards plain HTTP to the Service inside the cluster.
The nginx Pod is exactly the one from the previous example and knows nothing
about TLS.

```
internet --HTTPS--> Gateway (Envoy, holds the certificate) --HTTP--> Service --> Pods
```

This is the usual arrangement: certificates live in one place, owned by
whoever operates the Gateway, and applications stay unaware of them. The
alternative, `tls.mode: Passthrough`, forwards the encrypted stream untouched
to the backend, which then needs the certificate itself — useful for mutual
TLS or non-HTTP protocols, out of scope here.

## What "self-signed" means, and what it costs

A certificate binds a public key to a hostname, and is *signed* by someone.
For a public site, that someone is a certificate authority (CA) your browser
already trusts, and the trust chain is what makes the padlock green.

A self-signed certificate signs itself: it is its own authority. The
encryption on the wire is exactly the same — the traffic is as private as with
a paid certificate — but no client trusts the signature out of the box, so
every browser shows a full-page warning and `curl` refuses the connection
unless told otherwise. And no tool renews it: when it expires, HTTPS breaks
until someone regenerates it by hand.

So it is fine for a local cluster, a demo, a CI environment, or an internal
service whose (few) clients can be given the certificate explicitly — and
unusable for a public website, which is what the next example solves.

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

- **`openssl`** (1.1.1 or later, for the `-addext` option), to create the
  certificate.

No domain name is required: `my-app.example.com` is used throughout and
resolved locally, with `curl --resolve` or an `/etc/hosts` entry.

## Create the certificate

Generate a private key and a self-signed certificate valid for one year:

```shell
openssl req -x509 -newkey rsa:2048 -sha256 -days 365 -nodes \
  -keyout tls.key -out tls.crt \
  -subj "/CN=my-app.example.com/O=snippet-tls-demo" \
  -addext "subjectAltName=DNS:my-app.example.com"
```

- `-x509` makes it a self-signed certificate rather than a signing request
  (a CSR, which is what you would send to a real CA);
- `-nodes` ("no DES") leaves the private key unencrypted, which is required:
  the Gateway reads it without anyone typing a passphrase;
- `-subj "/CN=..."` fills the subject, mostly for humans nowadays;
- `-addext "subjectAltName=DNS:..."` is the part that actually matters.
  Clients have ignored the Common Name for hostname validation for years and
  only look at the Subject Alternative Name (SAN). A certificate without a SAN
  is rejected by every modern browser and by `curl`. Add one `DNS:` entry per
  hostname, comma-separated (`DNS:my-app.example.com,DNS:www.example.com`),
  or `IP:` entries to cover a bare address.

Look at what was produced:

```shell
openssl x509 -in tls.crt -noout -text | head -20
```

Or just the fields that matter here — note that issuer and subject are
identical, which is the definition of self-signed:

```shell
openssl x509 -in tls.crt -noout -subject -issuer -dates -ext subjectAltName
```

Keep `tls.key` private: anyone holding it can impersonate the site. It is
listed in `.gitignore` here, and both files stay out of the manifests.

## Put it in a Secret

The Gateway reads the certificate from a Secret of the dedicated type
`kubernetes.io/tls`, which must hold exactly two keys, `tls.crt` and
`tls.key`. Create the namespace and the Secret:

```shell
kubectl create namespace snippet-tls-demo

kubectl create secret tls my-tls \
  --cert=tls.crt --key=tls.key \
  -n snippet-tls-demo
```

Check the type and the two keys (`kubectl` shows their size, not their
content):

```shell
kubectl describe secret my-tls -n snippet-tls-demo
```

Read the certificate back out of the cluster, to confirm it is the same one:

```shell
kubectl get secret my-tls -n snippet-tls-demo \
  -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -subject -dates
```

This Secret is created imperatively on purpose. The declarative equivalent
exists — `kubectl create secret tls ... --dry-run=client -o yaml > secret.yml`
— but its content is merely base64-encoded, not encrypted, so committing it
would publish the private key in clear text (see
[`1.4.1_secret`](../1.4.1_secret/)) — actually storing a secret in git needs
a dedicated tool: SOPS, Sealed Secrets, or an external secret store.

## Deploy the demo

`deployment.yml` and `service.yml` are unchanged from the previous example.
What is new is in `gateway.yml`, which gains a second listener:

```yaml
- name: https
  protocol: HTTPS
  port: 443
  hostname: my-app.example.com
  tls:
    mode: Terminate
    certificateRefs:
      - name: my-tls
```

`certificateRefs` points at the Secret by name. It has no `namespace` field
here because the Secret sits in the Gateway's own namespace; referring to a
Secret in another namespace is possible but requires a `ReferenceGrant` in
that namespace, granting the permission explicitly.

The `hostname` on a listener is what lets several HTTPS sites, each with its
own certificate, share one Gateway and one IP address: the client announces
the hostname it wants through SNI (Server Name Indication) during the TLS
handshake, and the proxy picks the matching listener and certificate. Which
is also why the tests below all have to set that hostname explicitly.

`http-route.yml` now attaches to the `https` listener through `sectionName`
and declares the matching `hostnames`. `http-redirect-route.yml` handles the
plain HTTP listener with a `RequestRedirect` filter and no backend at all: the
Gateway answers `301` by itself, so nothing is ever served in clear text.

Apply everything:

```shell
kubectl apply \
  -f deployment.yml \
  -f service.yml \
  -f gateway.yml \
  -f http-route.yml \
  -f http-redirect-route.yml \
  -n snippet-tls-demo
```

Wait for the Gateway's `PROGRAMMED` column to show `True` and its `ADDRESS` to
be populated (`Ctrl+C` to stop watching):

```shell
kubectl get gateway -n snippet-tls-demo --watch
```

If `PROGRAMMED` stays `False`, the certificate reference is the first thing to
check — a missing or mistyped Secret leaves the HTTPS listener unresolved, and
the reason appears in the per-listener conditions:

```shell
kubectl describe gateway my-gateway -n snippet-tls-demo
```

Check the routes were accepted too:

```shell
kubectl get httproute -n snippet-tls-demo
kubectl describe httproute my-route -n snippet-tls-demo
```

## Test it

Store the address, used by every command below:

```shell
GATEWAY_IP=$(kubectl get gateway my-gateway -n snippet-tls-demo -o jsonpath='{.status.addresses[0].value}')
echo $GATEWAY_IP
```

(On a cloud cluster this is a public load balancer address. On a local
cluster, whether an address is assigned and reachable depends on the cluster's
LoadBalancer support — MetalLB, `minikube tunnel`, or `cloud-provider-kind`
for kind.)

`--resolve` makes `curl` send requests for `my-app.example.com` to that
address, without touching DNS. Try it first without any special flag, and
watch it fail:

```shell
curl --resolve my-app.example.com:443:$GATEWAY_IP https://my-app.example.com/
```

```
curl: (60) SSL certificate problem: self-signed certificate
```

That is the whole point of a self-signed certificate: the connection is
encrypted, but nothing vouches for the identity behind it. Two ways forward.

Skip verification entirely, which is the lazy one — never in a script that
matters, as it also disables detection of a real man-in-the-middle:

```shell
curl -k --resolve my-app.example.com:443:$GATEWAY_IP https://my-app.example.com/
```

Or hand `curl` the certificate as the trust anchor, which is the honest way to
use a self-signed certificate: the client is told, out of band, exactly which
certificate to expect. This is the nginx welcome page over a verified
connection:

```shell
curl --cacert tls.crt --resolve my-app.example.com:443:$GATEWAY_IP https://my-app.example.com/
```

Check the redirect on port 80 — `301` with a `location:` header pointing to
`https://`, and no page content:

```shell
curl -I --resolve my-app.example.com:80:$GATEWAY_IP http://my-app.example.com/
```

Add `-L` (follow redirects) to walk the whole path a browser would:

```shell
curl -L --cacert tls.crt \
  --resolve my-app.example.com:80:$GATEWAY_IP \
  --resolve my-app.example.com:443:$GATEWAY_IP \
  http://my-app.example.com/
```

Look at the certificate the Gateway actually serves, straight from the
handshake (`-servername` sets the SNI, exactly what `--resolve` lets `curl`
do):

```shell
openssl s_client -connect $GATEWAY_IP:443 -servername my-app.example.com </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates
```

To use a browser, point the hostname at the Gateway in `/etc/hosts`:

```shell
echo "$GATEWAY_IP my-app.example.com" | sudo tee -a /etc/hosts
```

Then open `https://my-app.example.com/`. The browser shows a warning page
(`NET::ERR_CERT_AUTHORITY_INVALID` or similar) which you can click through,
and the padlock stays crossed out. Clicking the padlock shows the certificate,
issued by itself. Remove the `/etc/hosts` line when you are done.

Making the warning go away for good means adding `tls.crt` to the trust store
of each machine that connects — the system store, or the browser's own — which
is exactly the work a public CA saves you, and why it does not scale beyond a
handful of machines.

## Renewal

The certificate expires after the 365 days set above, and nothing will renew
it. When that day comes, HTTPS simply stops working until someone runs the
`openssl` command again and replaces the Secret:

```shell
kubectl create secret tls my-tls \
  --cert=tls.crt --key=tls.key \
  -n snippet-tls-demo \
  --dry-run=client -o yaml | kubectl apply -f -
```

The Gateway picks up the new content on its own — the Secret is watched, and
the Envoy proxy is reconfigured without a restart.

This manual step is the reason cert-manager exists, and
[`5.2_lets_encrypt`](../5.2_lets_encrypt/) replaces this whole page with an
annotation on the Gateway. Note that cert-manager can also issue *self-signed*
certificates, through a `SelfSigned` Issuer, which keeps the automatic renewal
without needing a public domain — a good option for internal services.

## Remove the demo

```shell
kubectl delete \
  -f http-redirect-route.yml \
  -f http-route.yml \
  -f gateway.yml \
  -f service.yml \
  -f deployment.yml \
  -n snippet-tls-demo

kubectl delete secret my-tls -n snippet-tls-demo
kubectl delete namespace snippet-tls-demo
rm -f tls.crt tls.key
```

The GatewayClass and the Envoy Gateway controller are cluster-wide and shared
with every other Gateway on the cluster. **Do not delete them if you did not
install them, or if anything else still uses them.** Check first, and see
[`4.3.1_gateway_api_envoy_gateway`](../4.3.1_gateway_api_envoy_gateway/README.md#shared-resources-stop-and-check-first)
for the details:

```shell
kubectl get gateway --all-namespaces \
  -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,CLASS:.spec.gatewayClassName'
```

If that list is empty:

```shell
kubectl delete -f gateway-class.yml
helm uninstall eg --namespace envoy-gateway-system
```
