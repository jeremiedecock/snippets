# Gateway API: several apps behind one Gateway (with Envoy Gateway)

This example builds on [`4.3.1_gateway_api_envoy_gateway`](../4.3.1_gateway_api_envoy_gateway/),
which served a single application. Here, **two applications share a single
Gateway**, each in its own namespace, and traffic is routed to one or the other
based on the requested hostname.

This is the usual way to expose several HTTP applications with the Gateway API:
one entry point for the whole cluster, provisioned once, that every team plugs
into. It is also where the Gateway API clearly improves on Ingress, because the
split into three resources maps onto three different roles:

- **GatewayClass** — which controller implementation handles the traffic
  (installed once per cluster, like an IngressClass);
- **Gateway** — a listening entry point: address, port, protocol
  (managed by the cluster operator);
- **HTTPRoute** — the routing rules from a Gateway to a Service
  (managed by the application developer).

With Ingress, every team writes a full Ingress object and the cluster operator
has no say in it. Here, the operator owns the Gateway and decides which
namespaces may attach to it, while each application team owns only its own
HTTPRoute, in its own namespace.

Traffic flows as follows: internet → Gateway (a single proxy managed by the
controller) → the Service (ClusterIP) selected by the matching HTTPRoute →
Pods.

## Layout

Unlike the previous examples, the manifests are split into **one directory per
namespace**, and every manifest hardcodes its `metadata.namespace` (as in
[`1.2_pod_with_hardcoded_namespace`](../1.2_pod_with_hardcoded_namespace/)), so
no `-n` flag is needed when applying them:

```
gateway-class/gateway-class.yml   # cluster-wide, belongs to no namespace
gateway/                          # namespace snippet-gatewayapi-demo-gateway
├── namespace.yml
└── gateway.yml
app1/                             # namespace snippet-gatewayapi-demo-app1
├── namespace.yml
├── deployment.yml
├── service.yml
└── http-route.yml
app2/                             # namespace snippet-gatewayapi-demo-app2
├── namespace.yml
├── deployment.yml
├── service.yml
└── http-route.yml
```

The two applications are deliberately identical (a stock nginx server), so that
the only thing this example demonstrates is the routing. Each one is reachable
under its own hostname:

| Hostname           | Namespace                        |
| ------------------ | -------------------------------- |
| `app1.example.com` | `snippet-gatewayapi-demo-app1`   |
| `app2.example.com` | `snippet-gatewayapi-demo-app2`   |

The demo namespaces are all prefixed with `snippet-gatewayapi-demo-` to keep
them together and easy to clean up. In a real cluster, the Gateway namespace
would rather be named something like `gateway-infra`.

## Attaching a route to a Gateway in another namespace

Each HTTPRoute lives next to the application it routes to, and points at the
shared Gateway through `parentRefs`:

```yaml
parentRefs:
  - name: my-gateway
    namespace: snippet-gatewayapi-demo-gateway
    sectionName: http
```

`sectionName` names the Gateway *listener* to attach to. It is optional while
the Gateway has a single listener, but becomes necessary as soon as a second
one is added (an HTTPS listener, for instance).

Crossing a namespace boundary like this is not allowed by default: the Gateway
must opt in, through the listener's `allowedRoutes`:

```yaml
allowedRoutes:
  namespaces:
    from: All
```

`All` accepts routes from any namespace, which keeps this demo short. The two
other values are `Same` (only routes in the Gateway's own namespace) and
`Selector` (only namespaces carrying a given label) — the latter is the usual
production choice, and `gateway/gateway.yml` carries it as a commented-out
alternative. This is the knob Ingress never had: the cluster operator, not the
application teams, decides who may use the shared entry point.

Note that no `ReferenceGrant` is involved here. A ReferenceGrant is required
for a cross-namespace **`backendRef`** (a route forwarding to a Service in
another namespace); the attachment of a route to a Gateway is governed solely
by `allowedRoutes` on the Gateway side. In this example, each HTTPRoute
forwards to a Service in its own namespace, so nothing else is needed.

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
second one: note its name, set `spec.gatewayClassName` in
`gateway/gateway.yml` accordingly (the manifests here assume `eg`), and skip
the `apply` below.

Otherwise, deploy the GatewayClass, which binds the `eg` class name to the
Envoy Gateway controller:

```shell
kubectl apply -f gateway-class/gateway-class.yml
```

Check that the class exists and has been accepted by the controller (the
`ACCEPTED` column should show `True`; `False` or `Unknown` usually means the
controller is not installed or not running):

```shell
kubectl get gatewayclass
```

See the [Envoy Gateway documentation](https://gateway.envoyproxy.io/docs/install/install-helm/)
for more installation options.

## Deploy the demo

Each manifest carries its own namespace, so the manifests only have to be
applied in dependency order: the namespace first, then the rest.

Create the shared Gateway:

```shell
kubectl apply \
  -f gateway/namespace.yml \
  -f gateway/gateway.yml
```

Envoy Gateway then creates an Envoy proxy Deployment and a LoadBalancer Service
for it (in the `envoy-gateway-system` namespace). Wait for the `PROGRAMMED`
column to show `True` and the `ADDRESS` column to be populated (press `Ctrl+C`
to stop watching):

```shell
kubectl get gateway -n snippet-gatewayapi-demo-gateway --watch
```

Deploy the first application:

```shell
kubectl apply \
  -f app1/namespace.yml \
  -f app1/deployment.yml \
  -f app1/service.yml \
  -f app1/http-route.yml
```

And the second one:

```shell
kubectl apply \
  -f app2/namespace.yml \
  -f app2/deployment.yml \
  -f app2/service.yml \
  -f app2/http-route.yml
```

Check that both applications are ready:

```shell
kubectl get all,httproute -n snippet-gatewayapi-demo-app1
kubectl get all,httproute -n snippet-gatewayapi-demo-app2
```

Confirm that both routes were accepted by the shared Gateway. Each HTTPRoute
lists the Gateway it attached to in its `PARENTREFS` column, and its status
conditions say whether the attachment succeeded — this is where a rejection
by `allowedRoutes` would show up:

```shell
kubectl describe httproute my-route -n snippet-gatewayapi-demo-app1
```

## Query the two applications

Both applications answer on the Gateway's single address, so the hostname is
what selects between them. `app1.example.com` and `app2.example.com` are not
real domains, so send the `Host` header by hand:

```shell
kubectl get gateway -n snippet-gatewayapi-demo-gateway   # read the ADDRESS column
curl -H "Host: app1.example.com" http://<ADDRESS>/
curl -H "Host: app2.example.com" http://<ADDRESS>/
```

Both return the same nginx welcome page, since the two applications are
identical. To actually see that the two requests were served by two different
Pods, watch the access logs of each Deployment while running the curl commands
above:

```shell
kubectl logs -f -n snippet-gatewayapi-demo-app1 deployment/my-deployment
kubectl logs -f -n snippet-gatewayapi-demo-app2 deployment/my-deployment
```

An unknown hostname matches no HTTPRoute, and the Gateway answers `404`:

```shell
curl -i -H "Host: app3.example.com" http://<ADDRESS>/
```

On a cloud cluster, the address is typically provided by a public load
balancer. On a local cluster, whether an address is assigned and reachable
depends on the cluster's LoadBalancer support (e.g. MetalLB, `minikube tunnel`,
or `cloud-provider-kind` for kind).

## Remove the demo

Deleting a namespace deletes everything inside it, so the three namespaces are
enough to remove the applications and the Gateway:

```shell
kubectl delete namespace \
  snippet-gatewayapi-demo-app1 \
  snippet-gatewayapi-demo-app2 \
  snippet-gatewayapi-demo-gateway
```

Envoy Gateway removes the Envoy proxy Deployment and its LoadBalancer Service
along with the Gateway.

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
kubectl delete -f gateway-class/gateway-class.yml
```

This does not uninstall the Envoy Gateway controller, which serves every
Gateway on the cluster. Remove it only if you installed it for this example
and the command above listed no other Gateway — any Gateway left behind would
stop being reconciled and lose its Envoy proxy:

```shell
helm uninstall eg --namespace envoy-gateway-system
```
