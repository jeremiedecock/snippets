# Sealed Secrets

`9_secret_base64` ended on an uncomfortable note: a Secret is only
**base64-encoded, which is not encryption**. That weakness has two distinct
consequences, and they need two different fixes — a very common confusion:

| Problem | Where the plaintext is | Fix |
| --- | --- | --- |
| 1. Secret in **git** | in `secret.yml`, readable by anyone with repo access | **this example**, or SOPS / Ansible Vault |
| 2. Secret in **etcd** | on the control-plane disk, readable by anyone with a backup | `9_secret_etcd_encryption_at_rest` |

This example solves problem 1 only — as do its two siblings. Problem 2 is a
cluster-administrator concern, treated separately in
`9_secret_etcd_encryption_at_rest`.

Same app and same image as `9_secret_base64` (`hello-fastapi:3.0` — nothing to
rebuild): only the way the secret *reaches* the cluster changes.

## How it works

[Sealed Secrets](https://github.com/bitnami/sealed-secrets) uses **asymmetric
encryption**:

- a controller in the cluster holds a **private** key;
- the `kubeseal` CLI encrypts your Secret with the matching **public** key,
  producing a `SealedSecret` resource;
- only that controller can decrypt it, and it does so to create the real
  `Secret` in the cluster.

The consequence is what makes it useful: a `SealedSecret` is **safe to commit
to a public repository**. Even the person who created it cannot decrypt it
back. The value is also bound to the target name *and* namespace by default,
so a sealed secret cannot be copied into another namespace to be read there.

Why this one? [External Secrets
Operator](https://external-secrets.io/) is more widely deployed overall, but
it needs an external secret manager (Vault, AWS/GCP/Azure, OVHcloud) — Sealed
Secrets is self-contained and runs on a laptop cluster, which suits this repo.
See `9_secret_git_external_secrets_ovh` for the ESO route.
[SOPS](https://github.com/getsops/sops) (CNCF, integrated with Flux and
ArgoCD) is the other common choice; it encrypts values inside files rather
than adding a cluster resource — see `9_secret_git_sops`, which also
compares the three side by side. A fourth option, for those who already deploy
with Ansible, is Ansible Vault (`9_secret_git_ansible_vault`).

## 1. Install the controller and the CLI

The controller, with [Helm](https://helm.sh/) (the `fullnameOverride` matters:
`kubeseal` looks for a controller named `sealed-secrets-controller` in
`kube-system` by default):

```
helm repo add sealed-secrets https://bitnami.github.io/sealed-secrets
helm repo update
helm install sealed-secrets sealed-secrets/sealed-secrets \
  -n kube-system --set-string fullnameOverride=sealed-secrets-controller
```

The `kubeseal` CLI — `brew install kubeseal`, or on Linux:

```
KUBESEAL_VERSION=0.38.4
curl -OL "https://github.com/bitnami/sealed-secrets/releases/download/v${KUBESEAL_VERSION}/kubeseal-${KUBESEAL_VERSION}-linux-amd64.tar.gz"
tar -xzf "kubeseal-${KUBESEAL_VERSION}-linux-amd64.tar.gz" kubeseal
sudo install -m 755 kubeseal /usr/local/bin/kubeseal
```

## 2. Seal the secret

Note that this repo contains **no `secret.yml`** — that is the whole point.
Build the Secret on the fly and pipe it straight into `kubeseal`, so the
plaintext never touches the disk:

```
kubectl create secret generic hello \
  --from-literal=token=s3cr3t-t0k3n \
  --dry-run=client -o yaml \
  | kubeseal --format yaml > sealedsecret.yml
```

(`--dry-run=client` means "produce the manifest, do not send it to the
cluster". `kubeseal` fetches the controller's public key by itself; with
`--fetch-cert` you can save that certificate and seal secrets offline, with no
cluster access at all.)

Open the generated `sealedsecret.yml`: `spec.encryptedData.token` is now an
unreadable ciphertext. This file replaces `secret.yml` in git.

## 3. Deploy

`kubectl apply -f configmap.yml -f sealedsecret.yml -f deployment.yml -f service.yml`

The controller decrypts the SealedSecret and creates a normal Secret named
`hello`, which is why `deployment.yml` is **byte-for-byte identical** to the
one in `9_secret_base64`: the app knows nothing about any of this.

```
kubectl get sealedsecret,secret hello
```

Use it: `kubectl port-forward service/hello 8080:80`, then
`curl http://localhost:8080/` → the token appears, exactly as in
`9_secret_base64`.

## What this does *not* fix

```
kubectl get secret hello -o jsonpath='{.data.token}' | base64 -d
```

... still prints the token. The Secret that ends up in the cluster is an
ordinary Secret: Sealed Secrets protects the *manifest*, not the object.
Anyone whose RBAC rights allow reading Secrets in that namespace can still
read it — **RBAC is what controls access**, encryption never replaces it. And
that Secret is written to etcd in plaintext unless the cluster enables
encryption at rest (`9_secret_etcd_encryption_at_rest`).

Two operational consequences: back up the controller's private key (otherwise
a lost cluster means unrecoverable sealed secrets), and rotate the secret
values themselves, since sealing does not expire them.

```
kubectl get secret -n kube-system -l sealedsecrets.bitnami.com/sealed-secrets-key -o yaml > main.key   # keep offline!
```

Delete everything: `kubectl delete -f configmap.yml -f sealedsecret.yml -f deployment.yml -f service.yml`
(deleting the SealedSecret also deletes the Secret it generated).
