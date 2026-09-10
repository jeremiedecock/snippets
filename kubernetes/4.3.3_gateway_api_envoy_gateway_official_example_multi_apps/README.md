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

```
kubectl apply -f infra/gateway.yml                       # ONLY IF NOT ALREADY APPLIED!
kubectl create ns snippet-gatewayapi-demo1
kubectl create ns snippet-gatewayapi-demo2
kubectl apply -f app1/ -n snippet-gatewayapi-demo1
kubectl apply -f app2/ -n snippet-gatewayapi-demo2
kubectl get service -n envoy-gateway-system              # Get the public IP address of the Envoy Gateway (`EXTERNAL-IP` column)
curl -v -H "Host: demo1.example.com" http://YOUR_PUBLIC_IP/get
curl -v -H "Host: demo2.example.com" http://YOUR_PUBLIC_IP/get
kubectl delete -f app1/ -n snippet-gatewayapi-demo1
kubectl delete -f app2/ -n snippet-gatewayapi-demo2
kubectl delete ns snippet-gatewayapi-demo1
kubectl delete ns snippet-gatewayapi-demo2
```
