# PostgreSQL: the standard way to share state

The two previous examples showed the dilemma of a file-based database:
unsynchronized copies (`11_sqlite_volume`) or a single replica
(`12_pv_pvc`). The standard solution is to move the state into a **database
server**: [PostgreSQL](https://www.postgresql.org/) is designed for many
clients writing concurrently over the network, so the backend Pods become
*stateless* again — replicated, load-balanced, disposable — and the state
has a single source of truth.

The architecture (each arrow is a Service):

```
browser → frontend (nginx ×2) → backend (FastAPI ×3, stateless) → db (PostgreSQL ×1) → PVC
```

Note how the lessons of the previous examples combine: the `db` component is
a Deployment with `replicas: 1` + `Recreate` + a PVC (exactly the
`12_pv_pvc` pattern — fine here, because PostgreSQL is *made* to be the
single writer on its files), a ClusterIP Service gives it the stable DNS name
`db` (`10_fullstack`), and its credentials live in a Secret (`9_secret_base64`),
injected both into PostgreSQL (`POSTGRES_PASSWORD`) and into the backend
(`DATABASE_URL` — the password appears in two keys of `secret.yml`, kept
simple on purpose; and as always, this file is only committed because the
values are fake).

## Build and push the backend image

Version `5.0` talks to PostgreSQL through the
[psycopg](https://www.psycopg.org/) driver instead of opening a SQLite file
(the frontend `2.0` image is unchanged):

```
cd backend
podman build -t docker.io/your-username/hello-fastapi:5.0 .
podman push docker.io/your-username/hello-fastapi:5.0
```

## Deploy

Edit `your-username` in `backend.yml`, then:

`kubectl apply -f secret.yml -f db.yml -f backend.yml -f frontend.yml`

Wait for everything to be ready (`kubectl get pods` — the backend may restart
once or twice if it comes up before PostgreSQL: it reconnects at every
request, so the order does not matter).

Use it: `kubectl port-forward service/frontend 8080:80`, open
`http://localhost:8080`, Save, then click Read repeatedly: `served_by` cycles
through the backend Pods, but the message is now **always the same** — and it
survives Pod deletions, node reschedulings, and even a full redeploy, since
it lives in PostgreSQL's PVC.

The backend can scale freely again: `kubectl scale deployment backend --replicas=5`

Look inside the database directly:

```
kubectl exec -it deployment/db -- psql -U hello -d hello -c "SELECT * FROM messages;"
```

Delete everything:
`kubectl delete -f secret.yml -f db.yml -f backend.yml -f frontend.yml`
(deleting the PVC deletes the data).

## In real life

This is the right *pattern*, but a self-hosted single-replica PostgreSQL is
the bare minimum, not a production setup. For real workloads, either use your
cloud provider's managed database (RDS, Cloud SQL...) — the cluster then only
holds the stateless parts — or run PostgreSQL with a dedicated operator like
[CloudNativePG](https://cloudnative-pg.io/), which manages replication,
failover and backups. (Stateful workloads with per-replica identity and
storage are also what the StatefulSet resource — not covered here — is for.)
