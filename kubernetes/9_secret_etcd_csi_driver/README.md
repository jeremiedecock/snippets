# Secrets Store CSI Driver (no Secret object at all)

The three "encrypted" siblings all protect the secret *on its way to the
cluster*, then hand a perfectly ordinary Secret to Kubernetes — which stores
it in etcd. `9_secret_etcd_encryption_at_rest` fixes that by encrypting what
etcd receives. This example takes the other road: **never create a Secret**,
so there is nothing in etcd to protect.

The [Secrets Store CSI
Driver](https://secrets-store-csi-driver.sigs.k8s.io/) mounts secrets into the
Pod as **files on a tmpfs volume**, fetched directly from an external manager
(HashiCorp Vault here; AWS, GCP and Azure providers exist too). The value goes
from the manager to the Pod's memory, and never transits through the
Kubernetes API or etcd.

```
Vault  →  CSI driver (on the node)  →  tmpfs volume in the Pod  →  the app reads a file
```

## The price: the app must read files

This is not a drop-in replacement, and that is the honest lesson of this
example. `main.py` changed: the token is read from `/mnt/secrets/token`
instead of the `SECRET_TOKEN` environment variable, hence a new image
(`hello-fastapi:3.1` — a variant of the `3.0` from `9_secret_base64`, not a
step forward in the series).

The app reads the file **at every request**, which buys something an
environment variable cannot offer: when the secret rotates, the driver
rewrites the file in place and the new value is picked up with no restart.
Compare with `8_configmap`, where changing the value required
`kubectl rollout restart`.

## Prerequisites

### 1. The CSI driver

```
helm repo add secrets-store-csi-driver https://kubernetes-sigs.github.io/secrets-store-csi-driver/charts
helm repo update
helm install csi-secrets-store secrets-store-csi-driver/secrets-store-csi-driver \
  --namespace kube-system \
  --set enableSecretRotation=true
```

`enableSecretRotation` is **off** by default: without it the mounted file is
never refreshed after the Pod starts.

### 2. Vault, in dev mode, with its CSI provider

The driver is only a mechanism; it needs a *provider* plugin for the backend
you use. Vault ships one, and its dev mode makes this runnable on a laptop
cluster:

```
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update
helm install vault hashicorp/vault \
  --set "server.dev.enabled=true" \
  --set "injector.enabled=false" \
  --set "csi.enabled=true"
```

⚠️ **Dev mode is for learning only**: Vault runs in memory (everything is lost
on restart), starts unsealed, and uses a root token. A real deployment means
persistent storage, a proper unseal strategy and TLS.

### 3. Configure Vault

Store the secret, then let Vault trust the cluster's ServiceAccount tokens:

```
kubectl exec -it vault-0 -- sh

vault kv put secret/hello token=s3cr3t-t0k3n

vault auth enable kubernetes
vault write auth/kubernetes/config \
    kubernetes_host="https://$KUBERNETES_PORT_443_TCP_ADDR:443"

vault policy write hello - <<EOF
path "secret/data/hello" {
  capabilities = ["read"]
}
EOF

vault write auth/kubernetes/role/hello \
    bound_service_account_names=hello \
    bound_service_account_namespaces=default \
    policies=hello \
    ttl=20m

exit
```

Note what identifies the app: not a password, but **its ServiceAccount** —
`bound_service_account_names=hello` matches the `serviceAccountName: hello` in
`deployment.yml`. Any other workload gets refused, even in the same namespace.

### 4. Build and push the image

Version `3.1` reads the token from a file (details in `7_custom_image`):

```
podman build -t docker.io/your-username/hello-fastapi:3.1 .
podman push docker.io/your-username/hello-fastapi:3.1
```

## Deploy

Edit `your-username` in `deployment.yml`, then:

`kubectl apply -f configmap.yml -f secretproviderclass.yml -f deployment.yml -f service.yml`

Use it: `kubectl port-forward service/hello 8080:80`, then
`curl http://localhost:8080/` → the token appears, as in `9_secret_base64`.

## Check that nothing landed in etcd

This is the whole point of the example:

```
kubectl get secret hello
```

→ `Error from server (NotFound): secrets "hello" not found`. There is no
Secret object, so nothing to encrypt at rest, nothing to leak in a `kubectl
get secrets` listing, and nothing in an etcd backup.

The value does exist, as a file inside each Pod:

```
kubectl exec deployment/hello -- cat /mnt/secrets/token
kubectl exec deployment/hello -- mount | grep /mnt/secrets   # tmpfs, in memory
```

Rotation, if `enableSecretRotation=true` was set — change the value in Vault
and watch it reach the app without any restart (the default poll interval is
two minutes):

```
kubectl exec -it vault-0 -- vault kv put secret/hello token=rotated-t0k3n
curl http://localhost:8080/
```

Delete everything: `kubectl delete -f configmap.yml -f secretproviderclass.yml -f deployment.yml -f service.yml`

## Trade-offs

**In its favour** — the secret never reaches etcd, so encryption at rest
becomes moot for it; it is never exposed by `kubectl get secret`; it lives in
tmpfs rather than on disk; access is granted per workload identity
(ServiceAccount) instead of per namespace; and rotation propagates without a
restart.

**Against it** — the application must read files, which rules out software
that only takes environment variables (unless you re-enable `secretObjects`
sync, which recreates a Kubernetes Secret and cancels the benefit); Pod
startup now depends on the external manager being reachable, so Vault becomes
a hard dependency in the boot path; and there are considerably more moving
parts than a `kubectl apply`.

**RBAC still matters.** No Secret object means one less thing to protect, but
anyone able to `kubectl exec` into the Pod reads the file, and anyone able to
create a Pod with that ServiceAccount can mount the secret.

**In production**, the managed equivalents avoid running Vault yourself: the
AWS, GCP and Azure providers plug the same driver into Secrets Manager, Secret
Manager and Key Vault, and are offered as cluster add-ons on EKS, GKE and AKS.

Finally, remember the distinction from `9_secret_etcd_encryption_at_rest`: the
External Secrets Operator looks similar but *does* create a Kubernetes Secret,
so it lands in etcd. Only this approach keeps it out.
