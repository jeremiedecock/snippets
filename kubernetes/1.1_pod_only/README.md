# Pod

A Pod is the smallest deployable unit in Kubernetes: one or more containers
that always run together on the same node and share the same IP address.
Here the Pod contains a single container running the
[nginx](https://hub.docker.com/_/nginx) web server.

Create the namespace for the demo: `kubectl create namespace snippet-pod-demo`

Deploy the Pod: `kubectl apply -f pod.yml -n snippet-pod-demo`

Check that it is running: `kubectl get pods -n snippet-pod-demo` (wait for
`STATUS: Running`), and see the full details (node, IP, events...):
`kubectl describe pod my-pod -n snippet-pod-demo`

Use it: the Pod IP is only reachable from inside the cluster, so forward its
port to your machine with `kubectl port-forward -n snippet-pod-demo my-pod 8080:80`,
then open `http://localhost:8080` in a web browser.

Display its logs: `kubectl logs -f my-pod -n snippet-pod-demo` (each page load
adds a line)

Open a shell inside the container: `kubectl exec -it my-pod -n snippet-pod-demo -- sh`

Delete the Pod: `kubectl delete pod my-pod -n snippet-pod-demo`

Delete the namespace: `kubectl delete namespace snippet-pod-demo`

Note: a bare Pod like this one is never used in practice — if it crashes or
its node dies, nothing restarts it, and its IP changes every time it is
recreated. The next examples fix this step by step, with a Service (stable
address) and a Deployment (supervision, replication, self-healing).
