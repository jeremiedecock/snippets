# Gateway API (with Envoy Gateway)

The [Gateway API](https://gateway-api.sigs.k8s.io/) is the official successor
of the Ingress API. Ingress is feature-frozen, and its most popular controller,
ingress-nginx, was retired on March 24, 2026 (no more bug fixes or security
patches). New projects should use the Gateway API.

Where Ingress crammed everything into one resource (plus controller-specific
*annotations*), the Gateway API splits routing into three resources, matching
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
helm install eg oci://docker.io/envoyproxy/gateway-helm --version v1.9.1 -n envoy-gateway-system --create-namespace
```

Wait for Envoy Gateway to become available:

```
kubectl wait --timeout=5m -n envoy-gateway-system deployment/envoy-gateway --for=condition=Available
```

See [Envoy Gateway documentation](https://gateway.envoyproxy.io/docs/install/install-helm/) for more details.

Check that it is ready: `kubectl get pods -n envoy-gateway-system`

## Deploy

Create the namespace for the demo: `kubectl create namespace snippet-gatewayapi-demo`

Deploy everything: `kubectl apply -f deployment.yml -f service.yml -f gateway.yml -f httproute.yml -n snippet-gatewayapi-demo`

Find the public address (the `ADDRESS` column, may take a minute to appear —
Envoy Gateway creates a LoadBalancer Service and an Envoy proxy for each
Gateway): `kubectl get gateway hello`

Then retrieve the public address () using: `kubectl get gateway hello -n snippet-gatewayapi-demo`

And make a request to it: `curl -v -H "Host: demo.example.com" http://YOUR_PUBLIC_ADDRESS/get`

The usual caveat applies: on a cloud provider the address is a public
LoadBalancer IP; on a local cluster (minikube, kind, k3s on your laptop) it is
only reachable from your machine or your LAN.

Delete everything: `kubectl delete -f deployment.yml -f service.yml -f gateway.yml -f httproute.yml -n snippet-gatewayapi-demo`

Delete the namespace for the demo: `kubectl delete namespace snippet-gatewayapi-demo`

Note: to migrate existing Ingress manifests, the official
[ingress2gateway](https://github.com/kubernetes-sigs/ingress2gateway) tool
converts them to Gateway API resources automatically.
