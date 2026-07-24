# Encryption at rest (the secret in etcd)

`9_secret_base64` showed that a Secret is only **base64-encoded, which is not
encryption**. That weakness has two distinct consequences, and confusing them
is extremely common:

| Problem | Where the plaintext is | Fix |
| --- | --- | --- |
| 1. Secret in **git** | in `secret.yml`, readable by anyone with repo access | Sealed Secrets, SOPS or Ansible Vault — the three sibling examples |
| 2. Secret in **etcd** | on the control-plane disk, readable by anyone with a backup | **this example** |

Sealing, SOPS and Vault all protect the *manifest on its way to the cluster*.
Once applied, the object stored by the API server is an ordinary Secret,
written to etcd in plaintext — so **none of them solves problem 2**, and this
one is not solved by the application at all.

That is why this directory has no Deployment, no Service and no Secret:
nothing changes application-side. Encryption at rest is a **cluster
administrator** concern, configured on the API server, and it applies to every
Secret in the cluster at once, whatever produced them. Use the manifests of
`9_secret_base64` if you want an object to observe.

## What this actually protects against

Worth being precise, because the protection is narrower than it sounds:

| Threat | Protected? |
| --- | --- |
| Stolen etcd backup, or a snapshot of the etcd disk | **yes** — the main point |
| Attacker with root on a control-plane node | **no** with a local key (it is right there); **yes** with KMS |
| User with RBAC read access on Secrets | **no** — the API server decrypts transparently; only RBAC helps |

Encryption at rest is not access control. `kubectl get secret -o yaml` keeps
returning the value to anyone entitled to ask.

## Family A: encrypt what enters etcd

The native mechanism: an `EncryptionConfiguration` file
([documentation](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/))
given to the API server with `--encryption-provider-config=...`. The available
providers:

| Provider | Encryption | Notes |
| --- | --- | --- |
| `identity` | none | the default — no confidentiality at all |
| `aescbc` | AES-CBC | unauthenticated (no MAC), a weaker class of construction; still the default in k3s/RKE2, and the FIPS 140-2 option |
| `aesgcm` | AES-GCM | fast, but the key must be rotated roughly every 200k writes — only with automated rotation |
| `secretbox` | XSalsa20-Poly1305 | authenticated, fast; the sane default among local providers |
| `kms` v2 | envelope encryption | **the production recommendation** (GA since 1.29; v1 deprecated in 1.28, disabled by default in 1.29) |

Two example files here: `encryption-config.yml` (local `secretbox` key) and
`encryption-config-kms.yml` (KMS v2). Both are API-server config files, **not**
manifests — do not `kubectl apply` them.

**The catch with local providers.** `aescbc`, `aesgcm` and `secretbox` all
store the key **in that file, on the control-plane disk**, next to the etcd
data it protects. Anyone who can read the disk reads both. It is still worth
enabling — stolen backups and decommissioned disks are a real and common
vector — but it is not the same guarantee as `kms`, where the key material
stays in an external KMS or HSM and never touches the node.

### In practice, you rarely write this file

- **Managed clusters** — you cannot pass API-server flags, so the provider
  exposes it as a setting, backed by its own KMS: Application-layer secrets
  encryption on GKE (Cloud KMS), envelope encryption on EKS (AWS KMS), KMS
  etcd encryption on AKS (Key Vault). One option to turn on.
- **k3s** — start the server with `--secrets-encryption`; it generates
  `/var/lib/rancher/k3s/server/cred/encryption-config.json`, and
  `--secrets-encryption-provider` picks the provider (default `aescbc`).
  Manage it with `k3s secrets-encrypt status` / `rotate-keys`.
- **RKE2** — enabled by default (`aescbc`), with
  `rke2 secrets-encrypt status` / `rotate-keys`.
- **kubeadm / self-managed** — this is where you actually write the file and
  add the flag to the API server manifest.

### Enabling it does not encrypt what is already there

The configuration only applies to **future writes**. Existing Secrets stay in
plaintext in etcd until something rewrites them:

```
kubectl get secrets --all-namespaces -o json | kubectl replace -f -
```

The same command is what re-encrypts everything after a key rotation.

### Verifying

Read the raw value straight from etcd, bypassing the API server:

```
etcdctl get /registry/secrets/default/hello
```

Before, the token is plainly visible in the output. After, the value starts
with `k8s:enc:secretbox:v1:` (or `k8s:enc:aescbc:v1:`, `k8s:enc:kms:v2:`)
followed by ciphertext.

## Family B: never put the secret in etcd

The other approach — arguably the better one for sensitive workloads — is to
avoid creating a Kubernetes Secret at all, so there is nothing in etcd to
encrypt:

- **[Secrets Store CSI Driver](https://secrets-store-csi-driver.sigs.k8s.io/)**
  — a CSI volume mounts the secret into the Pod (tmpfs) straight from an
  external manager (Vault, AWS/GCP/Azure), described by a `SecretProviderClass`.
  ⚠️ Enabling its `secretObjects` sync recreates a Kubernetes Secret and
  defeats the entire purpose. Worked example: `9_secret_etcd_csi_driver`.
- **Vault Agent Injector** — a mutating webhook adds an init container and a
  sidecar that fetch from Vault and write to a shared in-memory volume.
- **Short-lived identities** (SPIFFE/SPIRE, cloud workload identity) — remove
  the long-lived secret instead of protecting it. Kubernetes already applies
  this to itself: since 1.22/1.24 ServiceAccount tokens are projected and
  time-bound, no longer stored as Secrets.

The price: the app must read **files** rather than environment variables, Pod
startup now depends on the external store, and there are more moving parts.

**A frequent confusion**: the External Secrets Operator does *not* belong
here. ESO reads an external manager and then **creates a native Kubernetes
Secret** — which lands in etcd like any other. That is precisely what
separates it from the CSI driver; compare `9_secret_git_external_secrets_ovh`
with `9_secret_etcd_csi_driver`.

## Defence in depth

Neither family removes the need for: strict **RBAC** (the only thing guarding
the live object), **encrypted etcd backups** and disk encryption, TLS between
etcd peers, restricted access to control-plane nodes, and audit logging. Also
prefer mounting secrets as files over environment variables — env vars leak
into crash dumps, child processes and debugging output.

## Recommendation

- **Managed cluster**: enable the provider's KMS option. One setting, covers
  the main vector.
- **Self-managed**: `kms` v2 with a real KMS. Failing that, `secretbox` —
  genuinely useful against backup theft, as long as you keep its limit in
  mind.
- **Sensitive workloads**: Secrets Store CSI Driver, so the value never
  reaches etcd.
- **Always**: RBAC and encrypted backups. Encryption at rest never replaces
  access control.
