# Deployment with Service

Same Deployment as [3.2_deployment](../3.2_deployment), now exposed through a
ClusterIP Service (c.f. [2.1_clusterip_service](../2.1_clusterip_service)) —
the same pattern used to expose a bare Pod, applied here to a Deployment. The
Service selects the Pods by their `app: my-app` label and its `targetPort`
matches the container's named port (`http`), so it now load-balances requests
across all replicas instead of pointing at a single Pod.

Note that the Pods no longer have a fixed name: each replica gets a generated
name like `my-deployment-5f7b8c9d4-xk2pq`.

## Deploy

Create the namespace for the demo: `kubectl create namespace snippet-deployment-demo`

Deploy everything: `kubectl apply -f deployment.yml -f service.yml -n snippet-deployment-demo`

See the replicas: `kubectl get pods -l app=my-app -n snippet-deployment-demo`

Check the Service and its endpoints: `kubectl get service my-service -n snippet-deployment-demo` and `kubectl get endpointslices -l kubernetes.io/service-name=my-service -n snippet-deployment-demo`

Use it from inside the cluster (a ClusterIP is not reachable from your machine):

```
kubectl run test --rm -it --restart=Never --image=curlimages/curl -n snippet-deployment-demo -- curl -s http://my-service
```

Or forward the Service port to your machine: `kubectl port-forward service/my-service 8080:80 -n snippet-deployment-demo`
(then open `http://localhost:8080`)

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
one, without downtime:

```
kubectl set image deployment/my-deployment my-container=docker.io/library/nginx:mainline-alpine-slim -n snippet-deployment-demo
kubectl rollout status deployment/my-deployment -n snippet-deployment-demo
kubectl rollout undo deployment/my-deployment -n snippet-deployment-demo   # roll back if needed
```

Since the Service selects Pods by label rather than by name, it keeps routing
traffic to whichever Pods are ready throughout all of the above — no manual
update needed.

Delete everything: `kubectl delete -f deployment.yml -f service.yml -n snippet-deployment-demo`

Delete the namespace: `kubectl delete namespace snippet-deployment-demo`
