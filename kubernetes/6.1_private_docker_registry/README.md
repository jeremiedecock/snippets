1. Créer un PAT (https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-with-a-personal-access-token-classic)
    - Scope: `read:packages`, `write:packages`, `delete:packages`, `repo`
    - Copier le token dans `.bashrc`: `export GHCR_TOKEN=ghp_...`
    - `echo $GHCR_TOKEN | podman login ghcr.io -u USERNAME --password-stdin`
2. Build and push the image to GitHub Container Registry (https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#pushing-container-images)
    - `podman build -t ghcr.io/jeremiedecock/hello-fastapi:1.0 .`
    - Optional: test locally
      - `podman run -p 8000:8000 ghcr.io/jeremiedecock/hello-fastapi:1.0`
      - Open a browser and navigate to `http://localhost:8000` to see the FastAPI welcome message.
    - `podman push ghcr.io/jeremiedecock/hello-fastapi:1.0`
    - Check the pushed image on GitHub Container Registry: https://github.com/jeremiedecock?tab=packages
3. Create the namespace for the demo: `kubectl create namespace snippet-registry-demo`
4. Create the secret for pulling the image from GitHub Container Registry
```
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username='jeremiedecock' \
  --docker-password="$GHCR_TOKEN" \
  -n snippet-registry-demo
```
5. Deploy the pod using the pushed image
    - `kubectl apply -f pod.yml -n snippet-registry-demo`
    - `kubectl get pods -n snippet-registry-demo`
    - `kubectl describe pod my-pod -n snippet-registry-demo`
    - `kubectl logs pod my-pod -n snippet-registry-demo`
    - `kubectl port-forward my-pod 8000:8000 -n snippet-registry-demo` then open a browser and navigate to `http://localhost:8000` to see the FastAPI welcome message.
6. Delete everything: `kubectl delete -f pod.yml -n snippet-registry-demo && kubectl delete secret ghcr-secret -n snippet-registry-demo`
7. Delete the namespace: `kubectl delete namespace snippet-registry-demo`
