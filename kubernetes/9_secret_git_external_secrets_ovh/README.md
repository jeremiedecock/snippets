# External Secrets Operator + OVHcloud Secret Manager

The most widely deployed of all these approaches, and the one the other
examples kept deferring to because it needs a component outside the cluster.
On **OVHcloud Managed Kubernetes Service (MKS)** that component now exists:
[OVHcloud Secret Manager](https://www.ovhcloud.com/fr/identity-security-operations/secret-manager/),
in beta since November 2025 and generally available since 15 January 2026,
built on OVHcloud KMS and hosted in French datacenters.

The [External Secrets Operator](https://external-secrets.io/) (ESO, a CNCF
project) watches `ExternalSecret` resources, fetches the values from the
manager, and creates ordinary Kubernetes Secrets from them.

```
OVHcloud Secret Manager  →  ESO (in the cluster)  →  a normal Secret  →  the app
```

## What makes it different from the other examples

**The secret value is never in git — not even encrypted.** Sealed Secrets,
SOPS and Ansible Vault all commit a ciphertext; here the repo contains only a
*pointer* (`remoteRef: key: hello`). Nothing to seal, re-encrypt or rekey.
Rotating the secret means changing it in Secret Manager: ESO picks it up
within `refreshInterval`, with no commit and no redeploy.

**It is a drop-in.** ESO produces a genuine Kubernetes Secret, so
`deployment.yml` is byte-for-byte identical to `9_secret_base64` and the
image is unchanged (`hello-fastapi:3.0`). Compare with
`9_secret_etcd_csi_driver`, which required rewriting the app to read files.

**But the secret does land in etcd.** That is the flip side of the drop-in
property, and the difference from the CSI driver: ESO *creates* a Secret
object, so problem 2 remains — pair this with
`9_secret_etcd_encryption_at_rest`.

## Manual prerequisites (OVHcloud side)

These steps happen in the OVHcloud console or CLI, once. They use the
[`ovhcloud` CLI](https://github.com/ovh/ovhcloud-cli); the console does the
same.

**1. Order a Secret Manager (OKMS) domain**, then note its region and id:

```
ovhcloud okms list
```

You get an `id` (a UUID) and a `region` such as `eu-west-par` or
`eu-west-rbx`. Both go into the ClusterSecretStore.

**2. Store the secret.** Create a secret named `hello` with a `token` field
holding `s3cr3t-t0k3n` (console: *Secret Manager → Create a secret*).

**3. Create an IAM identity and a Personal Access Token.** Grant only what
reading requires:

- `okms:apikms:secret/get`
- `okms:apikms:secret/version/getData`
- `okms:apiovh:secret/get`

(`okms:apikms:secret/create` is needed only if you also want to *write* from
the cluster, via ESO's `PushSecret`. Leave it out otherwise.)

```
ovhcloud iam user token create <user> \
  --name pat-secretmanager \
  --description "ESO read access for the MKS cluster"
```

Copy the returned token — it is shown once.

## Cluster side

**4. Install ESO:**

```
helm repo add external-secrets https://charts.external-secrets.io
helm repo update
helm install external-secrets external-secrets/external-secrets \
  -n external-secrets --create-namespace
```

(The chart installs and manages the CRDs by default; `--set installCRDs=false`
is only for GitOps setups where Argo CD or Flux applies them in a separate
wave.)

**5. Give ESO the token.** Create it imperatively so it never touches a file:

```
kubectl create secret generic ovh-token \
  -n external-secrets \
  --from-literal=token='<the-PAT-you-copied>'
```

This is the *secret zero* problem, and it is unavoidable with any external
manager: one bootstrap credential must live in the cluster so that everything
else can stay out of it. The trade is a good one — a single, rotatable,
narrowly-scoped token instead of every application secret. Using `mtls:`
authentication instead of a bearer token (see `clustersecretstore.yml`)
tightens it further.

**6. Point ESO at your domain.** Edit `clustersecretstore.yml` — replace
`REPLACE_WITH_YOUR_OKMS_ID` and the region — then:

```
kubectl apply -f clustersecretstore.yml
kubectl get clustersecretstore ovh-secret-manager   # STATUS should be Valid
```

Two variants are provided; apply **one**:

- `clustersecretstore.yml` — ESO's purpose-built `ovh` provider, which also
  supports mTLS;
- `clustersecretstore-vault.yml` — the `vault` provider, since OVHcloud Secret
  Manager speaks a Vault KV v2-compatible API. This is the path OVHcloud's own
  [documentation](https://docs.ovhcloud.com/en/guides/manage-and-operate/secret-manager/external-secret-operator)
  describes, and it ports unchanged to a real Vault.

## Deploy

`kubectl apply -f configmap.yml -f externalsecret.yml -f deployment.yml -f service.yml`

Watch ESO do its work — the `Secret` appears without ever having been written
by you:

```
kubectl get externalsecret hello    # STATUS: SecretSynced
kubectl get secret hello            # created by ESO, owned by the ExternalSecret
```

Use it: `kubectl port-forward service/hello 8080:80`, then
`curl http://localhost:8080/` → the token appears, exactly as in
`9_secret_base64`.

Now rotate it in Secret Manager and wait for `refreshInterval` (or force it
with `kubectl annotate externalsecret hello force-sync=$(date +%s) --overwrite`):
the value changes in the cluster with no commit, no `kubectl apply`, no
rebuild. That is the property none of the git-based approaches can offer.

Delete everything: `kubectl delete -f configmap.yml -f externalsecret.yml -f deployment.yml -f service.yml`
(deleting the ExternalSecret deletes the Secret it owns, per
`creationPolicy: Owner`).

## When to choose this

**In its favour** — no secret material in git in any form; central rotation
and revocation; audit logs and IAM on the manager side; one bootstrap
credential instead of many; and the same pattern works across clusters and
across environments, with the store as the only thing that changes. On
OVHcloud specifically, the data stays in French datacenters under European
jurisdiction, which is often the actual reason for choosing it.

**Against it** — it only makes sense if you already have (or want) a managed
secret store: a hard external dependency, a paid service, and a bootstrap
credential to look after. On a laptop cluster or a small self-hosted setup,
SOPS (`9_secret_git_sops`) gives you most of the benefit for none of the
infrastructure.

**A note on portability**: the same manifests work against AWS Secrets
Manager, GCP Secret Manager, Azure Key Vault, Vault, 1Password, Doppler and
others — only the `provider:` block of the ClusterSecretStore changes. The
`ExternalSecret` resources of your applications stay untouched, which is
precisely why ESO became the de facto standard.
