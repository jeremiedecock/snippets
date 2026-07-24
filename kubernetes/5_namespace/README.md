# Namespace

Same example as `4_gateway_api`, but everything runs in a dedicated
**Namespace** instead of the `default` one.

A Namespace groups related resources and isolates them from the rest of the
cluster: names only have to be unique within their namespace, and access
rights, quotas and network policies can be applied per namespace. The typical
use is one namespace per application, per team or per environment
(`myapp-staging`, `myapp-prod`...).

Two things changed compared to the previous example:

- a `Namespace` resource named `hello` (`namespace.yml`);
- every other resource declares `metadata.namespace: hello` — except the
  GatewayClass, which is *cluster-scoped* (it does not belong to any
  namespace, like Nodes or the Namespaces themselves).

## Deploy

Prerequisite: Envoy Gateway (see `4_gateway_api/README.md`).

Deploy everything (the namespace must be listed first, the other resources go
inside it): `kubectl apply -f namespace.yml -f deployment.yml -f service.yml -f gateway.yml -f httproute.yml`

`kubectl get` now shows nothing... because it looks at the `default` namespace.
Add `-n hello` to the commands of the previous examples:

```
kubectl get all -n hello
kubectl get gateway -n hello
```

(To avoid typing `-n hello` every time:
`kubectl config set-context --current --namespace=hello`)

As before, open `http://<ADDRESS>/` using the `ADDRESS` column of
`kubectl get gateway hello -n hello`.

Delete everything in one go — deleting a namespace deletes everything inside
it: `kubectl delete namespace hello` (plus `kubectl delete gatewayclass eg` if
you also want to remove the cluster-scoped GatewayClass).

Note: in production, a Gateway is often shared: it lives in an infrastructure
namespace, and application HTTPRoutes attach to it from their own namespaces
(this must be explicitly allowed with `allowedRoutes` on the Gateway
listener). Here the Gateway is inside the app namespace to keep the example
self-contained.
