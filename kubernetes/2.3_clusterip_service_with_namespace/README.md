# ClusterIP Service

A ClusterIP Service gives the Pod a stable virtual IP and a DNS name (`hello`),
reachable **from inside the cluster only**.
The Service finds the Pod thanks to the `app: hello` label (see `selector` in `service.yml`).

Deploy the Pod and the Service: `kubectl apply -f namespace.yml -f pod.yml -f service.yml`

Check the Service and its endpoints: `kubectl get service hello -n hello` and `kubectl get endpointslices -l kubernetes.io/service-name=hello -n hello`

Forward the Service port to your machine: `kubectl port-forward service/hello 8080:80 -n hello` (then open `http://localhost:8080`)

Delete everything: `kubectl delete -f pod.yml -f service.yml -f namespace.yml`
