# ClusterIP Service

A ClusterIP Service gives the Pod a stable virtual IP and a DNS name (`my-service`),
reachable **from inside the cluster only**.
The Service finds the Pod thanks to the `app: my-app` label (see `selector` in `service.yml`).

Deploy the Pod and the Service: `kubectl apply -f namespace.yml -f pod.yml -f service.yml`

Check the Service and its endpoints: `kubectl get service my-service -n my-namespace` and `kubectl get endpointslices -l kubernetes.io/service-name=my-service -n my-namespace`

Use it from inside the cluster (a ClusterIP is not reachable from your machine):

```
kubectl run test --rm -it --restart=Never --image=curlimages/curl -n my-namespace -- curl -s http://my-service
```

Or forward the Service port to your machine: `kubectl port-forward service/my-service 8080:80 -n my-namespace` (then open `http://localhost:8080`)

Delete everything: `kubectl delete -f pod.yml -f service.yml -f namespace.yml`
