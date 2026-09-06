1. Créer un PAT (https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-with-a-personal-access-token-classic)
    - Scope: `read:packages`, `write:packages`, `delete:packages`
    - Copier le token dans `.bashrc`: `export GHCR_TOKEN=ghp_...`
    - `echo $GHCR_TOKEN | podman login ghcr.io -u USERNAME --password-stdin`
2. Build and push the image to GitHub Container Registry (https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#pushing-container-images)
    - `podman build -t ghcr.io/jeremiedecock/hello-fastapi:1.0 .`
    - Optional: test locally
      - `podman run -p 8000:8000 ghcr.io/jeremiedecock/hello-fastapi:1.0`
      - Open a browser and navigate to `http://localhost:8000` to see the FastAPI welcome message.
    - `podman push ghcr.io/jeremiedecock/hello-fastapi:1.0`
    - Check the pushed image on GitHub Container Registry: https://github.com/jeremiedecock?tab=packages
3. Create the secret for pulling the image from GitHub Container Registry
```
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username='jeremiedecock' \
  --docker-password="$GHCR_TOKEN"
```
4. Deploy the app using the pushed image
    - Install Traefik (c.f. `4.2_ingress_traefik/README.md`):
```
helm repo add traefik https://traefik.github.io/charts
helm repo update
helm install traefik traefik/traefik
```
    - `kubectl apply -f deployment.yml -f service.yml -f ingress.yml`
    - `kubectl get all` -> note the `EXTERNAL-IP` of the service `service/traefik`
    - Optional (as there is only one app running behind Traefik): Create the DNS record...
    - Test by opening a browser and navigating to the DNS record you created to see the FastAPI welcome message: https://<your-dns-record-or-external-ip>/docs
