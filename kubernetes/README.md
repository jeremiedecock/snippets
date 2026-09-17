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
   - [`6.1_private_docker_registry_ghcr`](6.1_private_docker_registry_ghcr/)
     — build and push **your own image** (a minimal FastAPI app) to a
     private registry: **GHCR**, the GitHub Container Registry
   - [`6.1_private_docker_registry_ovh`](6.1_private_docker_registry_ovh/)
     — the same image on the **OVHcloud Managed Private Registry**, a
     managed **Harbor**: projects, **robot accounts**, and the pull Secret
     they feed
   - [`6.2.1_stateless_backend_ingress_traefik`](6.2.1_stateless_backend_ingress_traefik/)
     — that image exposed to the internet, with a Deployment, a Service and a
     Traefik **Ingress**
   - [`6.2.2_stateless_backend_gateway_api_envoy_gateway`](6.2.2_stateless_backend_gateway_api_envoy_gateway/)
     — the same, with the **Gateway API** (Envoy Gateway) in place of the
     Ingress: the version to use for new work
   - [`6.3_stateless_backend_gateway_api_envoy_gateway_with_lets_encrypt`](6.3_stateless_backend_gateway_api_envoy_gateway_with_lets_encrypt/)
     — 6.2.2 and 5.2 combined: the same app served over **HTTPS**, with a
     Let's Encrypt certificate (cert-manager)
   - [`6.4_stateless_fullstack_app`](6.4_stateless_fullstack_app/) — a
     **fullstack app**: that backend plus an nginx **frontend** that calls
     it, both behind **one hostname** over HTTPS, split by **path** in a
     single HTTPRoute (`/api` and `/`) — which is what makes CORS a
     non-issue
7. Persistence
   - [`7.1_sqlite_volume`](7.1_sqlite_volume/) — naive persistence in a
     **hostPath volume**, and why it is broken
   - [`7.2_pv_pvc`](7.2_pv_pvc/) — real storage with a
     **PersistentVolumeClaim**... at the price of a single replica
   - [`7.3_postgresql`](7.3_postgresql/) — state in a **PostgreSQL** server:
     persistent *and* scalable

Prerequisites: a Kubernetes cluster (minikube, kind, k3s, or a cloud one —
step 5 requires a cloud one with a public IP), `kubectl`,
[Helm](https://helm.sh/) from step 4 on, and Podman or Docker plus an
account on a container registry (Docker Hub, GHCR, or an OVHcloud Managed
Private Registry) from step 6 on.
