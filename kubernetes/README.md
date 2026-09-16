# Kubernetes examples, step by step

A progression of minimal examples, each adding one concept on top of the
previous one. The app is a stock nginx web server up through the HTTPS
examples (5.x), then your own FastAPI app (plus a small nginx frontend from
6.4 on), starting with the custom image and private registry example (6.1).

1. **Pod** — the smallest deployable unit
   - [`1.1_pod_only`](1.1_pod_only/) — a bare Pod
   - [`1.2_pod_with_hardcoded_namespace`](1.2_pod_with_hardcoded_namespace/) —
     the same, with the namespace hardcoded in the manifest
   - [`1.3_config_map`](1.3_config_map/) — inject configuration into a Pod
     with a **ConfigMap**
   - [`1.4.1_secret`](1.4.1_secret/) — inject sensitive values into a Pod
     with a **Secret**, and see why base64 makes it barely secret at all
2. **Service** — a stable address for the Pod inside the cluster
   - [`2.1_clusterip_service`](2.1_clusterip_service/) — a **ClusterIP
     Service**
   - [`2.2_clusterip_service_with_named_port`](2.2_clusterip_service_with_named_port/)
     — the same, targeting the container's **named port**
   - [`2.3_clusterip_service_with_hardcoded_namespace`](2.3_clusterip_service_with_hardcoded_namespace/)
     — the same, with the namespace hardcoded in the manifest
3. **Deployment** — replaces the bare Pod: replication, self-healing,
   rolling updates
   - [`3.1_replica_set`](3.1_replica_set/) — a **ReplicaSet** first, to see
     what a Deployment manages underneath
   - [`3.2_deployment`](3.2_deployment/) — the **Deployment** itself
   - [`3.3_deployment_with_hardcoded_namespace`](3.3_deployment_with_hardcoded_namespace/)
     — the same, with the namespace hardcoded in the manifest
   - [`3.4_deployment_with_config_map`](3.4_deployment_with_config_map/) —
     the ConfigMap of step 1.3, consumed by a Deployment
   - [`3.5_deployment_with_service`](3.5_deployment_with_service/) — the
     Service of step 2.1, exposing a Deployment
4. Expose the app to the internet
   - Legacy **Ingress** API:
     - [`4.1_ingress_nginx`](4.1_ingress_nginx/) — ingress-nginx (**retired in
       March 2026**, kept for reference)
     - [`4.2_ingress_traefik`](4.2_ingress_traefik/) — Traefik (still
       maintained, default on k3s)
   - **Gateway API** (the official successor to Ingress), with Envoy Gateway:
     - [`4.3.1_gateway_api_envoy_gateway`](4.3.1_gateway_api_envoy_gateway/) —
       the basic example
     - [`4.3.2_gateway_api_envoy_gateway_multi_apps`](4.3.2_gateway_api_envoy_gateway_multi_apps/)
       — two apps, each in its own namespace, sharing a single Gateway and
       routed by hostname
5. **HTTPS**, and a first access control
   - [`5.1_tls`](5.1_tls/) — a **self-signed certificate**, created with
     `openssl` and served by the Gateway
   - [`5.2_lets_encrypt`](5.2_lets_encrypt/) — automatic, publicly trusted
     Let's Encrypt certificates (cert-manager)
   - [`5.3.1_basic_auth_in_envoy`](5.3.1_basic_auth_in_envoy/) — protect the
     app with a password, from an **htpasswd** file checked by the **Gateway**
   - [`5.3.2_basic_auth_in_nginx`](5.3.2_basic_auth_in_nginx/) — the same
     password, checked by **nginx itself** instead: portable across Gateway
     API implementations, and free of Envoy's SHA-1 limitation
   - [`5.4_lets_encrypt_multi_apps`](5.4_lets_encrypt_multi_apps/) — 4.3.2
     and 5.2 combined: **two apps, two domain names, two certificates**,
     behind a single public IP
   - [`5.5_lets_encrypt_DNS-01`](5.5_lets_encrypt_DNS-01/) — the same
     certificates proven by the **DNS-01 challenge** instead: no open port 80,
     **wildcard** certificates, and **any registrar** (cert-manager +
     **acme-dns**, delegated with one static CNAME)
6. Your own image, and multiple services communicating
   - [`6.1_private_docker_registry`](6.1_private_docker_registry/) — build
     and push **your own image** (a minimal FastAPI app) to a private
     registry (GHCR)
   - [`6.3.1_stateless_backend_and_basic_auth_in_fastapi`](6.3.1_stateless_backend_and_basic_auth_in_fastapi/)
     — the same app behind an Ingress, with **basic auth** handled in FastAPI
   - [`6.4_stateless_fullstack_app`](6.4_stateless_fullstack_app/) — **two
     services communicating** (nginx frontend + FastAPI backend)
7. Persistence
   - [`7.1_sqlite_volume`](7.1_sqlite_volume/) — naive persistence in a
     **hostPath volume**, and why it is broken
   - [`7.2_pv_pvc`](7.2_pv_pvc/) — real storage with a
     **PersistentVolumeClaim**... at the price of a single replica
   - [`7.3_postgresql`](7.3_postgresql/) — state in a **PostgreSQL** server:
     persistent *and* scalable

Step `9_secret_base64` leaves the secret exposed in two independent places,
and the follow-up examples are prefixed by the one they fix.

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

Prerequisites: a Kubernetes cluster (minikube, kind, k3s, or a cloud one —
step 5 requires a cloud one with a public IP), `kubectl`,
[Helm](https://helm.sh/) from step 4 on, and Podman or Docker plus a Docker
Hub (or GHCR) account from step 6 on.
