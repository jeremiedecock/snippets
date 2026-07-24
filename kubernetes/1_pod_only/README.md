Deploy the Pod: `kubectl apply -f hello.yml`

Use it: `kubectl port-forward hello 8080:80` (then open a web browser on `http://localhost:8080`)

Display logs: `kubectl logs -f hello`

Delete the Pod: `kubectl delete pod hello`
