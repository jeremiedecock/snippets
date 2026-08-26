# Deployment

Same app as the previous example, but the bare Pod is replaced by a
**Deployment**. This is how applications are actually run in Kubernetes: you
never create Pods directly.

A Deployment manages a set of identical Pods (created from `spec.template`) and
guarantees that `spec.replicas` of them are always running. The Service still
selects the Pods by their `app: hello` label, so it now load-balances requests
across all replicas.

Note that the Pods no longer have a fixed name: each replica gets a generated
name like `hello-5f7b8c9d4-xk2pq`.

## Deploy

Deploy everything: `kubectl apply -f namespace.yml -f deployment.yml -f service.yml`

See the replicas: `kubectl get pods -l app=hello -n hello`

Use it: `kubectl port-forward -n hello service/hello 8080:80` (then open
`http://localhost:8080`)

## What a Deployment gives you

**Self-healing** — delete a Pod and watch the Deployment immediately recreate it:

```
kubectl delete pod <one-of-the-pod-names> -n hello
kubectl get pods -l app=hello -n hello
```

**Scaling** — change the number of replicas (also works by editing `replicas` in
`deployment.yml` and re-applying):

```
kubectl scale deployment hello --replicas=5 -n hello
```

**Rolling updates** — change the image and Kubernetes replaces the Pods one by
one, without downtime:

```
kubectl set image deployment/hello hello=docker.io/library/nginx:mainline-alpine-slim -n hello
kubectl rollout status deployment/hello -n hello
kubectl rollout undo deployment/hello -n hello   # roll back if needed
```

Delete everything: `kubectl delete -f deployment.yml -f service.yml -f namespace.yml`
