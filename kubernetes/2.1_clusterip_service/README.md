# ClusterIP Service

A ClusterIP Service gives the Pod a stable virtual IP and a DNS name (`my-service`),
reachable **from inside the cluster only**.
The Service finds the Pod thanks to the `app: my-app` label (see `selector` in `service.yml`).

Create the namespace for the demo: `kubectl create namespace snippet-service-demo`

Deploy the Pod and the Service: `kubectl apply -f pod.yml -f service.yml -n snippet-service-demo`

Check the Service and its endpoints: `kubectl get service my-service -n snippet-service-demo` and `kubectl get endpointslices -l kubernetes.io/service-name=my-service -n snippet-service-demo`

Use it from inside the cluster (a ClusterIP is not reachable from your machine):

```
kubectl run test --rm -it --restart=Never --image=curlimages/curl -n snippet-service-demo -- curl -s http://my-service
```

Or forward the Service port to your machine: `kubectl port-forward service/my-service 8080:80 -n snippet-service-demo` (then open `http://localhost:8080`)

Delete everything: `kubectl delete -f pod.yml -f service.yml -n snippet-service-demo`

Delete the namespace: `kubectl delete namespace snippet-service-demo`
