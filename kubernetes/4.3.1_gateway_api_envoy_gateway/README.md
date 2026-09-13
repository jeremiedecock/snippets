# Gateway API (with Envoy Gateway)

The [Gateway API](https://gateway-api.sigs.k8s.io/) is the official successor
to the Ingress API. Ingress is feature-frozen, and its most popular controller,
ingress-nginx, was retired on March 24, 2026 (no more bug fixes or security
patches). New projects should use the Gateway API instead.

Whereas Ingress crams everything into a single resource (plus
controller-specific *annotations*), the Gateway API splits routing into three
resources, each owned by a different role:

- **GatewayClass** — which controller implementation handles the traffic
  (installed once per cluster, like an IngressClass);
- **Gateway** — a listening entry point: address, port, protocol
  (managed by the cluster operator);
- **HTTPRoute** — the routing rules from a Gateway to a Service
  (managed by the application developer).

Traffic flows as follows: internet → Gateway (a proxy managed by the
controller) → Service (ClusterIP) → Pods.

## Prerequisite: a Gateway API implementation

Like Ingress, these resources do nothing unless a controller implements them.
This example uses [Envoy Gateway](https://gateway.envoyproxy.io/), the most
popular standalone implementation, built on the
[Envoy](https://www.envoyproxy.io/) proxy (CNCF). Other implementations exist
(Cilium, Istio, Traefik, Kong, NGINX Gateway Fabric...) and the manifests below
would work with them too, except for the `controllerName` in the GatewayClass.

Install it with [Helm](https://helm.sh/). This also installs the Gateway API
CRDs (`Gateway`, `HTTPRoute`, etc.), which are not shipped with Kubernetes:

```shell
helm install eg oci://docker.io/envoyproxy/gateway-helm --version v1.9.1 -n envoy-gateway-system --create-namespace
```

Wait for the controller to become available:

```shell
kubectl wait --timeout=5m -n envoy-gateway-system deployment/envoy-gateway --for=condition=Available
```

Check that its pod is running:

```shell
kubectl get pods -n envoy-gateway-system
```

Deploy the GatewayClass, a cluster-wide resource that binds the `eg` class
name to the Envoy Gateway controller:

```shell
kubectl apply -f gateway-class.yml
```

See the [Envoy Gateway documentation](https://gateway.envoyproxy.io/docs/install/install-helm/)
for more installation options.

## Deploy the demo

Create the namespace for the demo:

```shell
kubectl create namespace snippet-gatewayapi-demo
```

Apply all four manifests:

```shell
kubectl apply \
  -f deployment.yml \
  -f service.yml \
  -f gateway.yml \
  -f httproute.yml \
  -n snippet-gatewayapi-demo
```

Check that the resources are ready:

```shell
kubectl get all,gateway,httproute -n snippet-gatewayapi-demo
```

For `my-gateway`, Envoy Gateway creates an Envoy proxy Deployment and a
LoadBalancer Service (in the `envoy-gateway-system` namespace). Wait for the
`PROGRAMMED` column to show `True` and the `ADDRESS` column to be populated
(press `Ctrl+C` to stop watching):

```shell
kubectl get gateway -n snippet-gatewayapi-demo --watch
```

Then open `http://<ADDRESS>/` in a browser or query it with curl. You should
get the nginx welcome page:

```shell
curl http://<ADDRESS>/
```

On a cloud cluster, the address is typically provided by a public load
balancer. On a local cluster, whether an address is assigned and reachable
depends on the cluster's LoadBalancer support (e.g. MetalLB, `minikube tunnel`,
or `cloud-provider-kind` for kind).

## Remove the demo

Delete every resource created by the manifests:

```shell
kubectl delete \
  -f httproute.yml \
  -f gateway.yml \
  -f service.yml \
  -f deployment.yml \
  -n snippet-gatewayapi-demo
```

Delete the namespace:

```shell
kubectl delete namespace snippet-gatewayapi-demo
```

Delete the GatewayClass (cluster-wide resource):

```shell
kubectl delete -f gateway-class.yml
```

This does not uninstall the Envoy Gateway controller. To remove it as well:

```shell
helm uninstall eg --namespace envoy-gateway-system
```
