# Nginx Ingress (retired — kept for reference)

> **Warning**: ingress-nginx was officially retired on March 24, 2026. The
> project is read-only: no more bug fixes and **no more security patches**. Do
> not use it for anything new — see `4_gateway_api` for its replacement. This
> example is kept for reference because many existing clusters still run it.

An Ingress exposes HTTP Services to the outside world through an *Ingress
controller*. The chain is: internet → Ingress controller → Service (ClusterIP)
→ Pods. An Ingress cannot point directly to Pods, which is why the ClusterIP
Service is still needed here.

## Prerequisite: an Ingress controller

The Ingress resource is just a routing rule; it does nothing unless an Ingress
controller runs in the cluster. To install [ingress-nginx](https://kubernetes.github.io/ingress-nginx/deploy/):

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
```

(On minikube, use `minikube addons enable ingress` instead.)

## Deploy

Deploy everything: `kubectl apply -f deployment.yml -f service.yml -f ingress.yml`

Find the public address (the `ADDRESS` column, may take a minute to appear):
`kubectl get ingress hello`

Then open `http://<ADDRESS>/` in a web browser.

Note: whether this address is really reachable from the public internet depends
on where the cluster runs. On a cloud provider (GKE, EKS, AKS, Scaleway, OVH...)
the controller gets a public LoadBalancer IP. On a local cluster (minikube,
kind, k3s on your laptop) the address is only reachable from your machine or
your LAN, unless you configure port forwarding on your router.

Delete everything: `kubectl delete -f deployment.yml -f service.yml -f ingress.yml`
