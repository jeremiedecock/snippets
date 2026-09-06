# ClusterIP Service

A ClusterIP Service gives the Pod a stable virtual IP and a DNS name (`hello`),
reachable **from inside the cluster only**.
The Service finds the Pod thanks to the `app: hello` label (see `selector` in `service.yml`).

Deploy the Pod and the Service: `kubectl apply -f pod.yml -f service.yml`

Check the Service and its endpoints: `kubectl get service hello` and `kubectl get endpointslices -l kubernetes.io/service-name=hello`

Use it from inside the cluster (a ClusterIP is not reachable from your machine):

```
kubectl run test --rm -it --restart=Never --image=curlimages/curl -- curl -s http://hello
```

Or forward the Service port to your machine: `kubectl port-forward service/hello 8080:80` (then open `http://localhost:8080`)

Delete everything: `kubectl delete -f pod.yml -f service.yml`
