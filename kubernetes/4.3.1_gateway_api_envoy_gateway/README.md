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

### Is it already installed?

Both the Gateway API CRDs and their controller are cluster-wide resources,
shared by every application on the cluster. Somebody else — another team, or
the cluster administrator — may have installed them already, so check before
installing anything.

Are the Gateway API CRDs (`Gateway`, `HTTPRoute`, etc., which are not shipped
with Kubernetes) present? An empty output, or a `NotFound` error, means they
are not:

```shell
kubectl api-resources --api-group=gateway.networking.k8s.io
```

Is a controller already running? Envoy Gateway installs itself into the
`envoy-gateway-system` namespace (a `NotFound` error means it is absent), and
`helm list` shows any other chart-installed implementation:

```shell
kubectl get deployments -n envoy-gateway-system
helm list --all-namespaces
```

If both the CRDs and an Envoy Gateway controller are already there, skip the
`helm install` below and go to the GatewayClass step. If the controller in
place is another implementation (Cilium, Istio, Traefik, Kong, NGINX Gateway
Fabric...), you can use it instead: the manifests of this example stay the
same, only the `controllerName` in the GatewayClass has to match it.

### Installing it

Install it with [Helm](https://helm.sh/). This also installs the Gateway API
CRDs:

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

### The GatewayClass

The GatewayClass is a cluster-wide resource too, shared by every Gateway on
the cluster, so here as well, check whether a suitable one already exists
before creating another:

```shell
kubectl get gatewayclass
```

If that list already has an entry whose `CONTROLLER` column reads
`gateway.envoyproxy.io/gatewayclass-controller`, reuse it rather than adding a
second one: note its name, set `spec.gatewayClassName` in `gateway.yml`
accordingly (the manifests here assume `eg`), and skip the `apply` below.

Otherwise, deploy the GatewayClass, which binds the `eg` class name to the
Envoy Gateway controller:

```shell
kubectl apply -f gateway-class.yml
```

This installs no software (no Pod, no Deployment): it only creates a single
`GatewayClass` object named `eg`, whose `controllerName` points to the Envoy
Gateway controller installed by Helm above. `Gateway` objects reference it
through `spec.gatewayClassName: eg` to tell Kubernetes which controller must
provision their proxy. Because `GatewayClass` is a cluster-wide (non-namespaced)
resource, the manifest has no `metadata.namespace` and any `-n` flag would be
ignored by `kubectl`.

Check that the class exists and has been accepted by the controller (the
`ACCEPTED` column should show `True`; `False` or `Unknown` usually means the
controller is not installed or not running):

```shell
kubectl get gatewayclass
```

Show its status conditions and events:

```shell
kubectl describe gatewayclass eg
```

Show the full object as stored in the cluster, i.e. `gateway-class.yml` plus
the fields added by Kubernetes (`uid`, `creationTimestamp`, the
`last-applied-configuration` annotation added by `apply`) and the `status`
block filled in by the controller:

```shell
kubectl get gatewayclass eg -o yaml
```

To confirm the resource is cluster-wide, check the `NAMESPACED` column:

```shell
kubectl api-resources | grep gatewayclass
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
  -f http-route.yml \
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
  -f http-route.yml \
  -f gateway.yml \
  -f service.yml \
  -f deployment.yml \
  -n snippet-gatewayapi-demo
```

Delete the namespace:

```shell
kubectl delete namespace snippet-gatewayapi-demo
```

### Shared resources: stop and check first

The GatewayClass and the Envoy Gateway controller are cluster-wide and shared.
**Do not delete them if you did not install them, or if anything else on the
cluster still uses them** — in particular if you skipped their installation
above because they were already present.

List every Gateway on the cluster, with the class each one uses. If any Gateway
other than this demo's shows up, stop here and leave both resources in place:

```shell
kubectl get gateway --all-namespaces \
  -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,CLASS:.spec.gatewayClassName'
```

If nothing else uses it, delete the GatewayClass:

```shell
kubectl delete -f gateway-class.yml
```

This does not uninstall the Envoy Gateway controller, which serves every
Gateway on the cluster. Remove it only if you installed it for this example
and the command above listed no other Gateway — any Gateway left behind would
stop being reconciled and lose its Envoy proxy:

```shell
helm uninstall eg --namespace envoy-gateway-system
```
