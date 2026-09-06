# Let's Encrypt TLS certificates (with cert-manager)

Same example as `5_namespace`, but the Gateway now also serves **HTTPS**, with
a free [Let's Encrypt](https://letsencrypt.org/) certificate that is obtained
— and renewed every ~60 days — automatically by
[cert-manager](https://cert-manager.io/).

How it works: cert-manager watches Gateways annotated with
`cert-manager.io/cluster-issuer`. For each HTTPS listener it requests a
certificate from Let's Encrypt, answers the ACME HTTP-01 challenge (it proves
control of the domain by serving a token at
`http://<domain>/.well-known/acme-challenge/...` through a temporary HTTPRoute
— this is why the port 80 listener must stay), stores the certificate in the
Secret named by `certificateRefs`, and renews it before it expires.

## Prerequisites

- Envoy Gateway (see `4_gateway_api/README.md`).
- A cluster whose Gateway gets a **public** IP (Let's Encrypt must be able to
  reach it from the internet — this example cannot work on a purely local
  cluster).
- A **domain name you own**, with a DNS `A` record pointing to the Gateway
  address (`kubectl get gateway hello -n hello`).
- cert-manager, installed with [Helm](https://helm.sh/), with its Gateway API
  support enabled:

```
helm install cert-manager oci://quay.io/jetstack/charts/cert-manager \
  --namespace cert-manager --create-namespace \
  --set crds.enabled=true \
  --set config.enableGatewayAPI=true
```

(cert-manager only checks for the Gateway API CRDs at startup: install it
*after* Envoy Gateway, or restart it with
`kubectl rollout restart deployment -n cert-manager`.)

## Deploy

1. Replace `hello.example.com` with your domain in `gateway.yml` and
   `httproute.yml`, and `you@example.com` with your email in
   `clusterissuer.yml` (Let's Encrypt uses it for expiry warnings).

2. Deploy everything:
   `kubectl apply -f namespace.yml -f clusterissuer.yml -f deployment.yml -f service.yml -f gateway.yml -f httproute.yml`

3. Watch cert-manager obtain the certificate (takes a minute or two):

```
kubectl get certificate -n hello -w
```

When `READY` becomes `True`, the certificate is in the `hello-tls` Secret and
`https://<your-domain>/` works... with a browser warning: the Gateway is
annotated with the `letsencrypt-staging` issuer, which delivers untrusted test
certificates. Always start with staging: the real server has strict
[rate limits](https://letsencrypt.org/docs/rate-limits/) (e.g. 5 failures per
hour), easy to hit while debugging a DNS or firewall problem.

4. Once staging works, switch to the real issuer: in `gateway.yml`, change the
   annotation to `cert-manager.io/cluster-issuer: letsencrypt`, then re-apply
   and watch the certificate be re-issued:

```
kubectl apply -f gateway.yml
kubectl get certificate -n hello -w
```

`https://<your-domain>/` now shows a valid padlock. Nothing else to do, ever:
cert-manager renews the certificate automatically ~30 days before expiry.

If the certificate stays not-ready, follow the trail of intermediate
resources: `kubectl describe certificaterequest,order,challenge -n hello`.

Delete everything: `kubectl delete namespace hello` and
`kubectl delete clusterissuer letsencrypt-staging letsencrypt` (plus
`kubectl delete gatewayclass eg` if wanted — ClusterIssuers and GatewayClasses
are cluster-scoped, so they survive the namespace deletion).
