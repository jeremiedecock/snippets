# Nginx Ingress (retired — kept for reference)

> **Warning**: ingress-nginx was officially retired on March 24, 2026. The
> project is read-only: no more bug fixes and **no more security patches**. Do
> not use it for anything new — see `4.3.1_gateway_api_envoy_gateway` for its replacement. This
> example is kept for reference because many existing clusters still run it.

An Ingress exposes HTTP Services to the outside world through an *Ingress
controller*. The chain is: internet → Ingress controller → Service (ClusterIP)
→ Pods. An Ingress cannot point directly to Pods, which is why the ClusterIP
Service is still needed here.

## Prerequisite: an Ingress controller

The Ingress resource is just a routing rule; it does nothing unless an Ingress
controller runs in the cluster.

Install [ingress-nginx](https://kubernetes.github.io/ingress-nginx/deploy/)
with [Helm](https://helm.sh/) — this is the procedure documented by OVHcloud in
[Installing NGINX Ingress Controller](https://docs.ovhcloud.com/en/guides/public-cloud/containers-orchestration/managed-kubernetes/install-nginx-ingress),
and it works the same way on any provider:

```
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm -n ingress-nginx install ingress-nginx ingress-nginx/ingress-nginx --create-namespace
```

`--create-namespace` creates the `ingress-nginx` namespace on the fly, so there
is nothing to create beforehand.

The chart installs a `LoadBalancer` Service named `ingress-nginx-controller`.
On a cloud provider this triggers the creation of a real load balancer, which
takes a minute or two and is billed as a separate resource.

The alternative, without Helm, is to apply the manifests published by the
project:

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
```

Check that the IngressClass exists before going further:
`kubectl get ingressclass` — it should list `nginx`, the value used in
`ingress.yml`.

## Find the controller's public IP

Everything that reaches the cluster from the outside goes through the
controller's LoadBalancer Service, so its address is *the* entry point of all
your Ingresses. Read it in the `EXTERNAL-IP` column of:

```
kubectl get svc -n ingress-nginx ingress-nginx-controller
```

```
NAME                       TYPE           CLUSTER-IP      EXTERNAL-IP      PORT(S)                      AGE
ingress-nginx-controller   LoadBalancer   10.3.123.45     51.210.0.42      80:31234/TCP,443:32123/TCP   2m
```

While the load balancer is still being provisioned the column shows
`<pending>`; just wait and run the command again. Some providers return a DNS
name instead of an IP address — use it the same way.

This is the address to point your DNS records at (an `A` record for an IP, a
`CNAME` for a hostname) once you serve real domain names.

## Deploy

Create the namespace for the demo: `kubectl create namespace snippet-ingress-demo`

Deploy everything: `kubectl apply -f deployment.yml -f service.yml -f ingress.yml -n snippet-ingress-demo`

Find the public address (the `ADDRESS` column, may take a minute to appear):
`kubectl get ingress my-ingress -n snippet-ingress-demo`

That address is the controller's `EXTERNAL-IP` found above: every Ingress in
the cluster shares the same entry point, and the controller tells them apart by
host and path.

Then open `http://<ADDRESS>/` in a web browser.

Note: whether this address is really reachable from the public internet depends
on where the cluster runs. On a cloud provider (GKE, EKS, AKS, Scaleway, OVH...)
the controller gets a public LoadBalancer IP. On a local cluster (kind, k3s on
your laptop) the address is only reachable from your machine or your LAN,
unless you configure port forwarding on your router.

Delete everything: `kubectl delete -f deployment.yml -f service.yml -f ingress.yml -n snippet-ingress-demo`

Delete the namespace: `kubectl delete namespace snippet-ingress-demo`

This leaves the controller in place. To remove it as well (and release the
billed load balancer):

```
helm -n ingress-nginx uninstall ingress-nginx
kubectl delete namespace ingress-nginx
```
