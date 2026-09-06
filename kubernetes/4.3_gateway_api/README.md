# Gateway API (with Envoy Gateway)

The [Gateway API](https://gateway-api.sigs.k8s.io/) is the official successor
of the Ingress API. Ingress is feature-frozen, and its most popular controller,
ingress-nginx, was retired on March 24, 2026 (no more bug fixes or security
patches). New projects should use the Gateway API.

Where Ingress crammed everything into one resource (plus controller-specific
annotations), the Gateway API splits routing into three resources, matching
three roles:

- **GatewayClass** — which controller implementation handles the traffic
  (installed once per cluster, like an IngressClass);
- **Gateway** — a listening entry point: address, port, protocol
  (managed by the cluster operator);
- **HTTPRoute** — the routing rules from a Gateway to a Service
  (managed by the application developer).

The chain is: internet → Gateway (a proxy managed by the controller) →
Service (ClusterIP) → Pods.

## Prerequisite: a Gateway API implementation

Like Ingress, these resources do nothing unless a controller implements them.
This example uses [Envoy Gateway](https://gateway.envoyproxy.io/), the most
popular standalone implementation, built on the
[Envoy](https://www.envoyproxy.io/) proxy (CNCF). Other implementations exist
(Cilium, Istio, Traefik, Kong, NGINX Gateway Fabric...) and the manifests below
would work with them too, except for the `controllerName` in the GatewayClass.

Install it with [Helm](https://helm.sh/) (this also installs the Gateway API
CRDs — `Gateway`, `HTTPRoute`, etc. — which are not shipped with Kubernetes):

```
helm install eg oci://docker.io/envoyproxy/gateway-helm --version v1.8.3 \
  -n envoy-gateway-system --create-namespace
```

Check that it is ready: `kubectl get pods -n envoy-gateway-system`

## Deploy

Deploy everything: `kubectl apply -f deployment.yml -f service.yml -f gateway.yml -f httproute.yml`

Find the public address (the `ADDRESS` column, may take a minute to appear —
Envoy Gateway creates a LoadBalancer Service and an Envoy proxy for each
Gateway): `kubectl get gateway hello`

Then open `http://<ADDRESS>/` in a web browser.

The usual caveat applies: on a cloud provider the address is a public
LoadBalancer IP; on a local cluster (minikube, kind, k3s on your laptop) it is
only reachable from your machine or your LAN.

Delete everything: `kubectl delete -f deployment.yml -f service.yml -f gateway.yml -f httproute.yml`

Note: to migrate existing Ingress manifests, the official
[ingress2gateway](https://github.com/kubernetes-sigs/ingress2gateway) tool
converts them to Gateway API resources automatically.
