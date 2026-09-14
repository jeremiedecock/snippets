# Secret (base64-encoded, not encrypted)

Same example as `3.4_deployment_with_config_map`, with one addition: the app also returns a token
read from the `SECRET_TOKEN` environment variable, injected from a
**Secret**. (A real application would obviously never expose its secrets in
an API response — here the point is just to *see* the injection work.)

A Secret is almost the same object as a ConfigMap — key/value pairs injected
as environment variables or mounted as files — but meant for sensitive values
(passwords, API tokens, TLS keys...). The separation lets Kubernetes and its
tooling treat them differently: stricter access rights (RBAC), optional
encryption at rest in etcd, values kept out of `kubectl describe` output,
files mounted in memory (tmpfs) rather than written to disk.

Two things to know:

- In a manifest, Secret values are **base64-encoded, which is NOT
  encryption** — anyone can decode them. It only makes arbitrary binary data
  representable in YAML. `secret.yml` uses the `stringData` field to write
  the value in plain text (Kubernetes encodes it at apply time); the encoded
  equivalent lives in the `data` field.
- **Never commit a real secret to git**, encoded or not. This `secret.yml` is
  committed only because the value is fake. In real life, secrets are created
  imperatively so they never land in a file —
  `kubectl create secret generic my-secret --from-literal=token=...` — or come
  from an external secret manager (Vault, cloud secret managers, Sealed
  Secrets, External Secrets Operator...).

## Build and push version 3.0

`main.py` changed again (details in `6.1_private_docker_registry`):

```
podman build -t docker.io/your-username/hello-fastapi:3.0 .
podman push docker.io/your-username/hello-fastapi:3.0
```

## Deploy

Create the namespace for the demo: `kubectl create namespace snippet-secret-demo`

Compared to `3.4_deployment_with_config_map`, `deployment.yml` uses the `3.0` tag and adds a
second `env` entry: `SECRET_TOKEN`, filled from the `token` key of the
`my-secret` Secret (`valueFrom.secretKeyRef` — note the symmetry with
`configMapKeyRef`). Edit `your-username`, then:

`kubectl apply -f configmap.yml -f secret.yml -f deployment.yml -f service.yml -n snippet-secret-demo`

Use it: `kubectl port-forward service/my-service 8080:80 -n snippet-secret-demo`,
then `curl http://localhost:8080/` →
`{"message":"Hello from the ConfigMap!","secret_token":"s3cr3t-t0k3n"}`

## Look at the Secret from the outside

```
kubectl get secret my-secret -o yaml -n snippet-secret-demo
```

The value appears under `data`, base64-encoded. Decode it:

```
kubectl get secret my-secret -o jsonpath='{.data.token}' -n snippet-secret-demo | base64 -d
```

Conclusion: anyone allowed to read the Secret object can read the value.
Secrets protect against *accidental* exposure, not against a user with read
access — restricting who can read them (RBAC, namespaces) is what actually
protects them.

The companion examples pick up exactly here, and they split along the two
distinct weaknesses this one exposes. The `9_secret_git_*` ones keep the
secret out of the repository — `sealed_secret`, `sops`, `ansible_vault` and
`external_secrets_ovh`. The `9_secret_etcd_*` ones deal with the plaintext
copy the API server writes to etcd — `encryption_at_rest` and `csi_driver`.

Delete everything: `kubectl delete -f configmap.yml -f secret.yml -f deployment.yml -f service.yml -n snippet-secret-demo`

Delete the namespace: `kubectl delete namespace snippet-secret-demo`
