# ReplicaSet

A ReplicaSet manages a set of identical Pods (created from `spec.template`)
and guarantees that `spec.replicas` of them are always running, selected by
their `app: my-app` label (see `selector`). Here it manages 2 replicas of a
single container running the [nginx](https://hub.docker.com/_/nginx) web
server.

In practice a ReplicaSet is never created directly: it only supports
self-healing and scaling, not rolling updates. A Deployment (c.f.
[3.2_deployment](../3.2_deployment)) creates and manages a ReplicaSet for you,
and additionally handles rollouts and rollback — this example only exists to
show what runs underneath a Deployment.

## Deploy

Create the namespace for the demo: `kubectl create namespace snippet-replicaset-demo`

Deploy the ReplicaSet: `kubectl apply -f replicaset.yml -n snippet-replicaset-demo`

See the replicas: `kubectl get pods -l app=my-app -n snippet-replicaset-demo`

## What a ReplicaSet gives you

**Self-healing** — delete a Pod and watch the ReplicaSet immediately recreate it:

```
kubectl delete pod <one-of-the-pod-names> -n snippet-replicaset-demo
kubectl get pods -l app=my-app -n snippet-replicaset-demo
```

**Scaling** — change the number of replicas (also works by editing `replicas`
in `replicaset.yml` and re-applying):

```
kubectl scale replicaset my-replica-set --replicas=5 -n snippet-replicaset-demo
```

Note: editing the Pod template (e.g. the container image) and re-applying does
**not** update the existing Pods — only new ones created afterwards use it.
This is the gap that Deployments fill with rolling updates.

Delete everything: `kubectl delete -f replicaset.yml -n snippet-replicaset-demo`

Delete the namespace: `kubectl delete namespace snippet-replicaset-demo`
