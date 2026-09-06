# Pod

A Pod is the smallest deployable unit in Kubernetes: one or more containers
that always run together on the same node and share the same IP address.
Here the Pod contains a single container running the
[nginx](https://hub.docker.com/_/nginx) web server.

Deploy the Pod: `kubectl apply -f pod.yml`

Check that it is running: `kubectl get pods` (wait for `STATUS: Running`),
and see the full details (node, IP, events...): `kubectl describe pod hello`

Use it: the Pod IP is only reachable from inside the cluster, so forward its
port to your machine with `kubectl port-forward hello 8080:80`, then open
`http://localhost:8080` in a web browser.

Display its logs: `kubectl logs -f hello` (each page load adds a line)

Open a shell inside the container: `kubectl exec -it hello -- sh`

Delete the Pod: `kubectl delete pod hello`

Note: a bare Pod like this one is never used in practice — if it crashes or
its node dies, nothing restarts it, and its IP changes every time it is
recreated. The next examples fix this step by step, with a Service (stable
address) and a Deployment (supervision, replication, self-healing).
