# Traefik Ingress

Same example as `4_ingress_nginx`, but with [Traefik](https://doc.traefik.io/traefik/)
as the Ingress controller instead of ingress-nginx.

Compare the two `ingress.yml` files: the only difference is
`ingressClassName: traefik` instead of `nginx`. This is the point of the
Ingress API — it is a standard Kubernetes resource, and the controller that
implements it is swappable. The chain is unchanged: internet → Traefik →
Service (ClusterIP) → Pods.

Unlike ingress-nginx, Traefik is still actively maintained, so it remains a
reasonable choice for existing Ingress manifests. But the Ingress API itself
is feature-frozen: for new work, prefer the Gateway API (`4_gateway_api` —
Traefik implements it too).

## Prerequisite: the Traefik controller

If you use **k3s**, Traefik is already installed — skip this step.

Otherwise, install it with [Helm](https://helm.sh/):

```
helm repo add traefik https://traefik.github.io/charts
helm repo update
helm install traefik traefik/traefik
```

Check that its IngressClass exists: `kubectl get ingressclass`

Note: only run one Ingress controller at a time while learning. If ingress-nginx
from the previous example is still installed, remove it first to avoid confusion.

## Deploy

Deploy everything: `kubectl apply -f deployment.yml -f service.yml -f ingress.yml`

Find the public address (the `ADDRESS` column, may take a minute to appear):
`kubectl get ingress hello`

Then open `http://<ADDRESS>/` in a web browser.

The same caveat as with nginx applies: on a cloud provider the address is a
public LoadBalancer IP; on a local cluster (minikube, kind, k3s on your laptop)
it is only reachable from your machine or your LAN.

Delete everything: `kubectl delete -f deployment.yml -f service.yml -f ingress.yml`
