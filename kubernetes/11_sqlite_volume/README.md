# Volumes: naive persistence with SQLite (and why it is broken)

The fullstack app from `10_fullstack` becomes stateful: the backend now
**saves** the message in a [SQLite](https://sqlite.org/) database
(`/data/messages.db`) and **reads** it back. The frontend gets an input field
and two buttons (Save / Read), and both responses show which backend Pod
answered (`served_by`).

A container's filesystem is **ephemeral**: every time a container (re)starts,
it starts from the pristine image — anything written inside is lost. To make
data survive, a **volume** must be mounted into the container. This example
uses the naive kind on purpose, to expose its limits:

- `emptyDir` — a scratch directory tied to the *Pod*: it survives container
  restarts but is deleted with the Pod. Useless for a database.
- `hostPath` (used here) — a directory on the *node* that hosts the Pod
  (`/var/lib/hello-data`). It survives Pod restarts... as long as the Pod
  lands on the same node.

## Build and push the new images

Backend `4.0` (SQLite read/write) and frontend `2.0` (Save/Read buttons) —
details in `7_custom_image`:

```
cd backend
podman build -t docker.io/your-username/hello-fastapi:4.0 .
podman push docker.io/your-username/hello-fastapi:4.0
cd ../frontend
podman build -t docker.io/your-username/hello-frontend:2.0 .
podman push docker.io/your-username/hello-frontend:2.0
```

## Deploy

Compared to `10_fullstack`, `backend.yml` adds the `volumes` (Pod level) and
`volumeMounts` (container level) blocks. Edit `your-username`, then:

`kubectl apply -f backend.yml -f frontend.yml`

Use it: `kubectl port-forward service/frontend 8080:80`, open
`http://localhost:8080`, type a message, **Save**, then click **Read**.

## See the problem

Check where the backend replicas run: `kubectl get pods -o wide` (the `NODE`
column).

Click **Read** repeatedly. The Service load-balances across the three backend
Pods, and each Pod opens the database of *its own node*:

- on a **multi-node cluster**, the Pods see different `/var/lib/hello-data`
  directories: the saved message only exists on the node whose Pod handled
  the Save. Depending on which Pod answers, you get your message or
  `(no message yet)` — several unsynchronized databases;
- on a **single-node cluster** (default minikube, kind, k3s), everything
  *seems* to work, because all Pods share the node's directory. This is the
  trap: the bug only shows up in production. (To reproduce it locally, create
  a multi-node cluster, e.g. kind with a config file listing one
  `control-plane` and two `worker` nodes.)

Even on a single node, `hostPath` is a bad idea: the data is welded to one
machine (lost if the node dies, invisible to Pods scheduled elsewhere), and
letting Pods write to a node's filesystem is a security hole (which is why
many managed clusters simply forbid `hostPath`). The next example fixes this
with real, node-independent storage: PersistentVolumes.

Delete everything: `kubectl delete -f backend.yml -f frontend.yml` (the
`/var/lib/hello-data` directories remain on the nodes — Kubernetes does not
manage a `hostPath`'s lifecycle, one more reason to avoid it).
