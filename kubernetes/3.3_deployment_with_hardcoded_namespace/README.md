# Deployment (hardcoded namespace)

Same Deployment as [3.2_deployment](../3.2_deployment), but the namespace is
now hardcoded in the manifest (`namespace: my-namespace` in `deployment.yml`)
and created from `namespace.yml`, instead of being created separately and
passed with `-n` on every command (c.f. [1.2_pod_with_hardcoded_namespace](../1.2_pod_with_hardcoded_namespace)
and [2.3_clusterip_service_with_hardcoded_namespace](../2.3_clusterip_service_with_hardcoded_namespace)
for the same pattern applied to a Pod and a Service).

## Deploy

Deploy the namespace and the Deployment: `kubectl apply -f namespace.yml -f deployment.yml`

See the replicas: `kubectl get pods -l app=my-app -n my-namespace`

See the ReplicaSet created for you: `kubectl get replicasets -n my-namespace`

Use it: `kubectl port-forward deployment/my-deployment 8080:80 -n my-namespace`
(then open `http://localhost:8080`)

## What a Deployment gives you

**Self-healing** — delete a Pod and watch the Deployment immediately recreate it:

```
kubectl delete pod <one-of-the-pod-names> -n my-namespace
kubectl get pods -l app=my-app -n my-namespace
```

**Scaling** — change the number of replicas (also works by editing `replicas` in
`deployment.yml` and re-applying):

```
kubectl scale deployment my-deployment --replicas=5 -n my-namespace
```

**Rolling updates** — change the image and Kubernetes replaces the Pods one by
one, without downtime:

```
kubectl set image deployment/my-deployment my-container=docker.io/library/nginx:mainline-alpine-slim -n my-namespace
kubectl rollout status deployment/my-deployment -n my-namespace
kubectl rollout undo deployment/my-deployment -n my-namespace   # roll back if needed
```

Delete everything: `kubectl delete -f deployment.yml -f namespace.yml`
