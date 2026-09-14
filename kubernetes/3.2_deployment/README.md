# Deployment

Same app as the previous example, but the ReplicaSet is now managed by a
**Deployment** instead of being created directly (c.f.
[3.1_replica_set](../3.1_replica_set)). This is how applications are actually
run in Kubernetes: you never create ReplicaSets — or Pods — directly.

A Deployment manages a ReplicaSet (created from `spec.template`), which in
turn guarantees that `spec.replicas` Pods are always running, selected by
their `app: my-app` label. On top of what a ReplicaSet gives you, a
Deployment also handles rolling updates and rollback.

## Deploy

Create the namespace for the demo: `kubectl create namespace snippet-deployment-demo`

Deploy the Deployment: `kubectl apply -f deployment.yml -n snippet-deployment-demo`

See the replicas: `kubectl get pods -l app=my-app -n snippet-deployment-demo`

See the ReplicaSet created for you: `kubectl get replicasets -n snippet-deployment-demo`

Use it: `kubectl port-forward deployment/my-deployment 8080:80 -n snippet-deployment-demo`
(then open `http://localhost:8080`) — without a Service, there is no single
stable address load-balancing across replicas (c.f.
[3.5_deployment_with_service](../3.5_deployment_with_service)).

## What a Deployment gives you

**Self-healing** — delete a Pod and watch the Deployment immediately recreate it:

```
kubectl delete pod <one-of-the-pod-names> -n snippet-deployment-demo
kubectl get pods -l app=my-app -n snippet-deployment-demo
```

**Scaling** — change the number of replicas (also works by editing `replicas` in
`deployment.yml` and re-applying):

```
kubectl scale deployment my-deployment --replicas=5 -n snippet-deployment-demo
```

**Rolling updates** — change the image and Kubernetes replaces the Pods one by
one, without downtime (this is what a bare ReplicaSet cannot do):

```
kubectl set image deployment/my-deployment my-container=docker.io/library/nginx:mainline-alpine-slim -n snippet-deployment-demo
kubectl rollout status deployment/my-deployment -n snippet-deployment-demo
kubectl rollout undo deployment/my-deployment -n snippet-deployment-demo   # roll back if needed
```

Delete everything: `kubectl delete -f deployment.yml -n snippet-deployment-demo`

Delete the namespace: `kubectl delete namespace snippet-deployment-demo`
