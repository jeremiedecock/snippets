# SOPS + age

Third way to solve "never commit a secret in plaintext", after Sealed Secrets
(`9_secret_git_sealed_secret`) and Ansible Vault
(`9_secret_git_ansible_vault`). [SOPS](https://getsops.io/) — Secrets
OPerationS, a CNCF project — encrypts **the values inside a file**, leaving
its structure readable. Same app and same image as `9_secret_base64`
(`hello-fastapi:3.0`): nothing to rebuild, and `deployment.yml` is again
unchanged.

Open `secret.enc.yml`: it is still a perfectly readable Kubernetes manifest —
`apiVersion`, `kind`, `metadata`, `type` are in the clear, and only the token
became `ENC[AES256_GCM,data:...]`. That is the property that makes SOPS
pleasant to live with: `git diff` shows *which* secret changed and in which
resource, code review still works, and a typo in `metadata.name` is still
visible. Compare with Sealed Secrets, where the whole payload is one opaque
blob.

SOPS supports several key backends (AWS/GCP/Azure KMS, HashiCorp Vault, PGP,
age). This example uses [age](https://age-encryption.org/): modern,
keyfile-based, no infrastructure — the usual choice outside cloud KMS.

## An important detail: age is asymmetric

`.sops.yaml` contains an age **public** key (the "recipient"). Anyone — a
developer, a CI job — can encrypt a new secret with it while being unable to
read the existing ones; only the holder of the private key can decrypt. That
is the same write-only capability Sealed Secrets gives you, and it is exactly
what Ansible Vault's shared password cannot offer.

The `sops:` block appended to the file also stores a **MAC** over the whole
document: if someone tampers with a plaintext field (say, redirects the Secret
to another name), decryption fails instead of silently succeeding.

## Setup

Install both tools (Homebrew: `brew install sops age`), or on Linux:

```
curl -sSL -o sops https://github.com/getsops/sops/releases/download/v3.13.3/sops-v3.13.3.linux.amd64
sudo install -m 755 sops /usr/local/bin/sops

curl -sSL -O https://github.com/FiloSottile/age/releases/download/v1.3.1/age-v1.3.1-linux-amd64.tar.gz
tar -xzf age-v1.3.1-linux-amd64.tar.gz
sudo install -m 755 age/age age/age-keygen /usr/local/bin/
```

The `secret.enc.yml` committed here was encrypted with a **demo key pair**.
Its private key is published below so the example actually runs — which of
course means it protects nothing, exactly like the fake token inside it:

```
mkdir -p ~/.config/sops/age
cat > ~/.config/sops/age/keys.txt <<'EOF'
# public key: age169mnf2y4tuj63ggmq6y60h9mkgw7cuml9kwxazeqwcv0hygfzu2qgs4zcx
AGE-SECRET-KEY-1RS6K7V586JVGZKSPUQQPC28M6TYQ4P39ZGK5YM5GJYWWYXF92D4STUW75N
EOF
chmod 600 ~/.config/sops/age/keys.txt
```

For your own project, generate a real key pair with `age-keygen -o key.txt`,
put its **public** key in `.sops.yaml`, and keep the private key out of git
(in a password manager, and in the CI runner's secret store). Losing it means
losing every encrypted value.

## Deploy

SOPS has no cluster-side component: you decrypt and pipe into `kubectl`.

```
kubectl apply -f configmap.yml -f service.yml -f deployment.yml
sops decrypt secret.enc.yml | kubectl apply -f -
```

Use it: `kubectl port-forward service/hello 8080:80`, then
`curl http://localhost:8080/` → the token appears, as in `9_secret_base64`.

## Daily operations

Edit in place — SOPS decrypts into `$EDITOR`, re-encrypts on save, and only
rewrites the values that actually changed:

```
sops edit secret.enc.yml
```

Encrypt a brand-new manifest (the rule in `.sops.yaml` applies automatically,
which is why no key is named on the command line):

```
sops encrypt --in-place secret.enc.yml
```

Rotate the data key, and add or remove a recipient (e.g. when someone joins or
leaves): update the `age:` line in `.sops.yaml`, then

```
sops updatekeys secret.enc.yml
```

`sops rotate --in-place secret.enc.yml` generates a fresh data key. As always,
re-encryption is not rotation of the *secret itself*: if the private key
leaked, change the token too.

## GitOps

This is where SOPS stands apart. **Flux** decrypts SOPS natively — put the age
private key in a cluster Secret and reference it in the Kustomization:

```yaml
spec:
  decryption:
    provider: sops
    secretRef:
      name: sops-age
```

**Argo CD** goes through a plugin ([KSOPS](https://github.com/viaduct-ai/kustomize-sops)
or argocd-vault-plugin). Either way the cluster reconciles straight from git,
with no human running a decrypt command — which neither Sealed Secrets'
workflow nor Ansible Vault's push model gives you in the same way.
[helm-secrets](https://github.com/jkroepke/helm-secrets) does the equivalent
for Helm values.

Delete everything: `kubectl delete -f configmap.yml -f service.yml -f deployment.yml`
and `kubectl delete secret hello`

## Choosing between the three

| | Sealed Secrets | SOPS + age | Ansible Vault |
| --- | --- | --- | --- |
| Cryptography | asymmetric | asymmetric | symmetric |
| Write-only capability | yes | yes | no |
| Encrypted file readable/diffable | no (opaque blob) | **yes** (values only) | yes with `encrypt_string` |
| Cluster-side component | a controller | none | none |
| Bound to one cluster | **yes** | no | no |
| GitOps (Flux/Argo) | native | **native** | no |
| Decrypt outside the cluster | impossible | possible (with the key) | possible |

The trade-off between the top two is mostly about where the private key
lives. **Sealed Secrets** keeps it inside the cluster and never lets it out:
nobody can decrypt a sealed secret locally, which is a real security
advantage, at the cost of being tied to that one cluster (rebuild it and every
sealed secret must be re-sealed). **SOPS** keeps the key with you or in a KMS:
portable across clusters and usable in CI, but the key now has to be managed
and distributed like any other credential.

For most new projects, SOPS with age or a cloud KMS is the best default —
readable diffs, no cluster dependency, first-class GitOps support. If you
already run Vault or a cloud secret manager, External Secrets Operator remains
the better fit.

And, one last time: **none of this encrypts Secrets at rest in etcd**. Once
decrypted, the object in the cluster is an ordinary Secret — see
`9_secret_etcd_encryption_at_rest`.
