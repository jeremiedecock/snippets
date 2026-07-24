# Kubernetes examples, step by step

A progression of minimal examples, each adding one concept on top of the
previous one. The app is a stock nginx web server named `hello` up to step 6,
then your own FastAPI app from step 7 on.

1. [`1_pod_only`](1_pod_only/) — a **Pod**, the smallest deployable unit
2. [`2_clusterip_service`](2_clusterip_service/) — a **Service** gives the Pod
   a stable address inside the cluster
3. [`3_deployment`](3_deployment/) — a **Deployment** replaces the bare Pod:
   replication, self-healing, rolling updates
4. [`4_gateway_api`](4_gateway_api/) — expose the app to the internet with the
   **Gateway API** (Envoy Gateway)
5. [`5_namespace`](5_namespace/) — the same, isolated in a dedicated
   **Namespace**
6. [`6_lets_encrypt`](6_lets_encrypt/) — **HTTPS** with automatic Let's
   Encrypt certificates (cert-manager)
7. [`7_custom_image`](7_custom_image/) — build and deploy **your own image**
   (a minimal FastAPI app)
8. [`8_configmap`](8_configmap/) — inject configuration with a **ConfigMap**
9. [`9_secret_base64`](9_secret_base64/) — inject sensitive values with a
   **Secret**, and see why base64 makes it barely secret at all
10. [`10_fullstack`](10_fullstack/) — **two services communicating**
    (HTML/nginx frontend + FastAPI backend)
11. [`11_sqlite_volume`](11_sqlite_volume/) — naive persistence in a
    **hostPath volume**, and why it is broken
12. [`12_pv_pvc`](12_pv_pvc/) — real storage with a
    **PersistentVolumeClaim**... at the price of a single replica
13. [`13_postgresql`](13_postgresql/) — state in a **PostgreSQL** server:
    persistent *and* scalable

Step 9 leaves the secret exposed in two independent places, and the follow-up
examples are prefixed by the one they fix.

**`9_secret_git_*` — the secret in the repository.** Four interchangeable
answers, so pick one:

- [`9_secret_git_sealed_secret`](9_secret_git_sealed_secret/) — **Sealed
  Secrets**: an in-cluster controller holds the private key
- [`9_secret_git_sops`](9_secret_git_sops/) — **SOPS + age**: the best default
  for a new project (readable diffs, native GitOps support)
- [`9_secret_git_ansible_vault`](9_secret_git_ansible_vault/) — **Ansible
  Vault**: if Ansible is already your deployment tool
- [`9_secret_git_external_secrets_ovh`](9_secret_git_external_secrets_ovh/) —
  **External Secrets Operator** + OVHcloud Secret Manager: the most widely
  used approach, and the only one of the four storing no secret material in
  git at all (needs a managed secret store)

**`9_secret_etcd_*` — the plaintext copy the API server writes to etcd**,
which none of the four above removes:

- [`9_secret_etcd_encryption_at_rest`](9_secret_etcd_encryption_at_rest/) —
  encrypt what etcd receives (`EncryptionConfiguration`, KMS); a
  cluster-administrator setting, with nothing to change application-side
- [`9_secret_etcd_csi_driver`](9_secret_etcd_csi_driver/) — **Secrets Store
  CSI Driver**: never create a Secret at all, mount it from Vault into the
  Pod (which, as a bonus, also keeps it out of git)

The two families are complementary, not competing: encryption at rest pairs
with any of the four above it.

Alternatives to step 4, using the legacy Ingress API instead of the Gateway
API:

- [`4_ingress_nginx`](4_ingress_nginx/) — ingress-nginx (**retired in March
  2026**, kept for reference)
- [`4_ingress_traefik`](4_ingress_traefik/) — Traefik (still maintained,
  default on k3s)

Prerequisites: a Kubernetes cluster (minikube, kind, k3s, or a cloud one —
step 6 requires a cloud one with a public IP), `kubectl`,
[Helm](https://helm.sh/) from step 4 on, and Podman or Docker plus a Docker
Hub (or quay.io) account from step 7 on.
